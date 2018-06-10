"""
Substitute hexadecimal with corresponding chars, parse arrays and substitute
literal values for references.

Author: Joshua Munn
Fri 25 May 14:25:22 BST 2018
"""

import re
import sys


def generate_linebreaks(lines, *args):
    """
    lines: list or str to split into tokens.
    *args: specify delimiters, (defaults to ';' if none specified)
    Wrapper for recur_split.
    Returns a list of tokens split on ';', or specified delimiters.
    """
    if not args:
        lines = recur_split(lines, ';')
    else:
        for delim in args:
            lines = recur_split(lines, delim)
    return lines


def recur_split(token, delim):
    """
    Splits token on delimiter, returns flat array of tokens.
    """
    if not token:
        return None
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


def parse_hexchars(lines):
    """
    Find hexadecimal chars and substitute them with corresponding characters.
    """
    hex_char_regexp = r'\\x(\d[0-9a-zA-Z]{1})'
    output = []
    for line in lines:
        new_line = line
        hex_char_match = re.search(hex_char_regexp, new_line)
        while hex_char_match:
            new_line = new_line.replace(hex_char_match.group(0),
                                        chr(int(hex_char_match.group(1), 16)))
            hex_char_match = re.search(hex_char_regexp, new_line)
        output.append(new_line)
    return output


def find_arrays(lines):
    """
    Read array declarations into a dict.
    """
    array_regexp = r'^(?:var)*\s*(\w+)\s*=\s*\[(.*)\]\s*'
    arrays = {}
    for line in lines:
        array_match = re.search(array_regexp, line)
        if array_match:
            arrays[array_match.group(1)] = array_match.group(2).replace('"', '').split(', ')
    return arrays


def substitute_array_references(arrays, lines):
    """
    create list of tuples with (arrayname, pattern('arrayname[x]'),
    to substitute array references with actual values (use with care - doesn't account for
    arrays mutated after declaration).
    """
    array_index_regexp = [(array_name,
                           re.compile(array_name +r'\[(\d+)\]'))
                          for array_name in arrays.keys()]
    parsed_indexes = []
    for line in lines:
        new_line = line
        for pattern in array_index_regexp:
            index_match = pattern[1].search(new_line)
            while index_match:
                new_line = (new_line.replace(index_match.group(0), '"' +
                                             arrays[pattern[0]][int(index_match.group(1))] + '"'))
                index_match = re.search(pattern[1], new_line)
        parsed_indexes.append(new_line)
    return parsed_indexes


def main():
    if len(sys.argv) < 3:
        print(f'\nUsage: $ python {__file__} INFILE OUTFILE\n')
        print('...INFILE: .js to parse for scrambled characters\n'
              '...OUTFILE: .txt')
        exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    with open(infile, 'r') as fd:
        lines = fd.readlines()
    if len(lines) == 1:
        lines = generate_linebreaks(lines, ';', ',')
    lines = parse_hexchars(lines)
    arrays = find_arrays(lines)
    #print(arrays)
    #lines = substitute_array_references(arrays, lines)
    with open(outfile, 'w') as fd:
        fd.write('\n'.join(lines))


if __name__ == '__main__':
    main()
