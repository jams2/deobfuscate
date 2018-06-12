"""
Substitute hexadecimal with corresponding chars, parse arrays and substitute
literal values for references.

Author: Joshua Munn
Fri 25 May 14:25:22 BST 2018
"""

import argparse
import re


def generate_linebreaks(tokens, *args):
    """
    tokens (list | str)
    *args (optional delimiters, defaults to ';')
    Wrapper for recur_split.
    Returns a list of tokens split on delim.
    """
    if not isinstance(tokens, str) and not isinstance(tokens, list):
        raise TypeError(f'Expected list or str, got {type(tokens)}')
    if not args:
        tokens = recur_split(tokens, ';')
    else:
        for delim in args:
            tokens = recur_split(tokens, delim)
    return tokens


def recur_split(token, delim):
    """
    token (list | str), delim (str)
    Splits token on delimiter, returns flat array of tokens.
    """
    if not token:
        return
    elif isinstance(token, str):
        if not delim in token:
            return [token]
        token = token.split(delim)
        for i in range(0, len(token)-1):
            token[i] += delim
        token = [x for x in token if x != '']
        return token
    elif isinstance(token, list):
        split_tokens = []
        for x in token:
            if x:
                split_tokens += recur_split(x, delim)
        return split_tokens


def parse_hexchars(tokens):
    """
    tokens (list)
    Find hexadecimal chars and substitute them with corresponding characters.
    """
    if not isinstance(tokens, list):
        raise TypeError(f'Expected list, got {type(tokens)}')
    hex_char_regexp = r'\\x(\d[0-9a-zA-Z]{1})'
    output = []
    for token in tokens:
        new_token = token
        hex_char_match = re.search(hex_char_regexp, new_token)
        while hex_char_match:
            new_token = new_token.replace(hex_char_match.group(0),
                                          chr(int(hex_char_match.group(1), 16)))
            hex_char_match = re.search(hex_char_regexp, new_token)
        output.append(new_token)
    return output


def find_arrays(tokens):
    """
    tokens (list)
    Read array declarations into a dict.
    """
    if not isinstance(tokens, list):
        raise TypeError(f'Expected list, got {type(tokens)}')
    array_regexp = r'^(?:var|let|const)*\s*(\w+)\s*=\s*\[(.*)\]\s*'
    arrays = {}
    for token in tokens:
        array_match = re.search(array_regexp, token)
        if array_match:
            array_name = array_match.group(1)
            arrays[array_name] = parse_arrays(
                [x.lstrip(' ') for x in array_match.group(2).split(',')])
    return arrays


def parse_arrays(token):
    """
    token (list)
    Handle arbitrarily nested lists
    """
    if not token:
        raise ValueError('Unexpected empty token.')
    elif not isinstance(token, list):
        raise TypeError(f'Expected list, got {type(token)}')
    parsed = []
    i = 0
    while i < len(token):
        if token[i].startswith('['):
            token[i] = token[i][1:]
            parsed.append(parse_arrays(token[i:]))
        elif token[i].endswith(']'):
            parsed.append(token[i][:-1])
            return parsed
        else:
            parsed.append(token[i])
        i += nested_len(parsed[-1])
    return parsed


def nested_len(tokens):
    """
    tokens (list | str)
    Count all items in list of lists (of lists...)
    """
    i = 0
    if isinstance(tokens, list):
        for token in tokens:
            if isinstance(token, list):
                i += nested_len(token)
            else:
                i += 1
    elif isinstance(tokens, str):
        i += 1
    else:
        raise TypeError(f'Expected str or list, got {type(tokens)}')
    return i


def substitute_array_references(tokens, arrays):
    """
    tokens (list), arrays (dict)
    Create list of tuples with (arrayname, pattern('arrayname[x]'),
    to substitute array references with actual values (use with care - doesn't account for
    arrays mutated after declaration).
    """
    if not isinstance(tokens, list) and not isinstance(tokens, str):
        raise TypeError(f'Expected str or list, got {type(tokens)}')
    elif isinstance(tokens, str):
        tokens = [tokens]
    array_index_regexp = [(array_name, re.compile(array_name + r'(?:\[\d+\])+'))
                          for array_name in arrays.keys()]
    parsed_tokens = []
    for token in tokens:
        new_token = token
        for pattern in array_index_regexp:
            index_match = pattern[1].search(new_token)
            while index_match:
                indices = get_indices(index_match[0])
                new_token = (new_token.replace(index_match[0],
                                               get_array_item(arrays[pattern[0]], indices)))
                index_match = re.findall(pattern[1], new_token)
        parsed_tokens.append(new_token)
    return parsed_tokens


def get_indices(match):
    """
    match (str): array reference
    Parse an (multidimensional) array reference, return a list of the indices.
    Example: 'array[1][2][3]' returns [1, 2, 3]
    """
    match = match[match.index('['):]
    indices = []
    curr_num = ''
    for char in match:
        if char == '[':
            curr_num = ''
        elif char.isnumeric():
            curr_num += char
        elif char == ']':
            indices.append(int(curr_num))
    return indices


def get_array_item(array, indices):
    """
    array (list), indices (list->int)
    Get item from (nested) list
    """
    for i in indices:
        array = array[i]
    return array


def main():
    """
    If options not specified, execute all methods.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='.js file to parse', type=str)
    parser.add_argument('outfile', type=str, nargs='?', default=False,
                        help='destination file, print to STDOUT if not specified.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--linebreaks', action='store_true',
                       help='insert linebreaks after ";", or specify delimiters with -d.')
    group.add_argument('-d', '--delimiter', nargs='+', metavar='<delim>',
                       help='space separated list of delimiters to break lines on. ' +
                       'characters such as ";" may need to be escaped.')
    parser.add_argument('-x', '--hex', action='store_true',
                        help='parse hex encoded characters to ascii.')
    parser.add_argument('-a', '--arrays', action='store_true',
                        help='substitute array references for declared values')
    parser.add_argument('-r', '--range', nargs=2, type=int, metavar=('<start>', '<end>'),
                        help='range of lines to parse (non-inclusive). ' +
                        'applied before other actions.')
    args = parser.parse_args()
    with open(args.infile, 'r') as fd:
        tokens = fd.readlines()
    if (not args.linebreaks and not args.delimiter and not args.hex and
            not args.arrays and not args.range):
        tokens = generate_linebreaks(tokens)
        tokens = parse_hexchars(tokens)
        tokens = substitute_array_references(tokens, find_arrays(tokens))
    else:
        if args.range:
            tokens = tokens[args.range[0], args.range[1]]
        if args.linebreaks:
            tokens = generate_linebreaks(tokens)
        elif args.delimiter:
            tokens = generate_linebreaks(tokens, *args.delimiter)
        if args.hex:
            tokens = parse_hexchars(tokens)
        if args.arrays:
            tokens = substitute_array_references(tokens, find_arrays(tokens))
    if args.outfile:
        with open(args.outfile, 'w') as fd:
            fd.write('\n'.join(tokens))
    else:
        for token in tokens:
            print(token)


if __name__ == '__main__':
    main()
