import pytest
from deobfuscate import deobfuscate


@pytest.mark.parametrize(('unparsed', 'expected'), (
    ('1;2', ['1;', '2']),
    ('1', ['1']),
    (';1', [';', '1']),
    ('1;2;3', ['1;', '2;', '3']),
    ('1;2;3;', ['1;', '2;', '3;']),
    ([], None),
    (['1'], ['1']),
    ([['1;2'], '3'], ['1;', '2', '3']),
    ([['1;2;'], '3;'], ['1;', '2;', '3;']),
    ([['1;2;', ['1', '2', '3']], '3;'], ['1;', '2;', '1', '2', '3', '3;']),
    ([[[]], [], [[[]]], []], []),
    (';;;', [';', ';', ';']),
    ([';'], [';']),
    ))
def test_recur_split(unparsed, expected):
    assert deobfuscate.recur_split(unparsed, ';') == expected


@pytest.mark.parametrize(('unparsed', 'expected'), (
    (';1', [';', '1']),
    ('1,2;3', ['1,2;', '3']),
    ('1;2;3', ['1;', '2;', '3']),
    ('1;2;3;', ['1;', '2;', '3;']),
    (['1'], ['1']),
    (['1;'], ['1;']),
    (';;;', [';', ';', ';']),
    ([';'], [';']),
    ([], None),
    ('1;', ['1;']),
    (['1;2', ['1;2;3']], ['1;', '2', '1;', '2;', '3']),
    ([['1;2;'], '3;'], ['1;', '2;', '3;']),
    ([['1;2;', ['1', '2', '3']], '3;'], ['1;', '2;', '1', '2', '3', '3;']),
    ))
def test_generate_linebreaks_no_delim(unparsed, expected):
    assert deobfuscate.generate_linebreaks(unparsed) == expected


def test_generate_linebreaks_error():
    with pytest.raises(TypeError):
        deobfuscate.generate_linebreaks({})


@pytest.mark.parametrize(('unparsed', 'delims', 'expected'), (
    ('1,2;3', [';', ','], ['1,', '2;', '3']),
    (['1'], [';', ','], ['1']),
    ([], [';', ','], None),
    ([';1,2;3,'], [';', ','], [';', '1,', '2;', '3,']),
    (['2;3,1,2;3,'], [';', ','], ['2;', '3,', '1,', '2;', '3,']),
    ([['2;3,1,2;3,'], ',1;2,'], [';', ','], ['2;', '3,', '1,', '2;', '3,', ',', '1;', '2,']),
    (';,;,;,', [';', ','], [';', ',', ';', ',', ';', ',']),
    ([[';,'], ';', [',', [';,']]], [';', ','], [';', ',', ';', ',', ';', ',']),
    (['123,1;:2:3', ';', '::', ['1', ',2']], [';', ':', ','],
     ['123,', '1;', ':', '2:', '3', ';', ':', ':', '1', ',', '2'])
    ))
def test_generate_linebreaks_delims(unparsed, delims, expected):
    assert deobfuscate.generate_linebreaks(unparsed, *delims) == expected


@pytest.mark.parametrize(('unparsed', 'expected'), (
        (['var o = "\x73\x65\x72\x69\x66"'], ['var o = "serif"']),
        (['\x43\x61\x6C\x69\x62\x72\x69'], ['Calibri']),
        (['\x43\x61\x6D\x62\x72\x69\x61'], ['Cambria']),
        (['\x48\x6F\x65\x66\x6C\x65\x72\x20{"\x54\x65\x78\x74"}'], ['Hoefler {"Text"}']),
        (['x55\x55\x74\x6F\x70\x69\x61'], ['x55Utopia']),
        (['55\x4C\x69\x62\x65\x72\x61\x74\x69\x6F\x6E\x20\x53\x65\x72\x69\x66'], ['55Liberation Serif']),
        ([''], ['']),
        ))
def test_parse_hexchars(unparsed, expected):
    assert deobfuscate.parse_hexchars(unparsed) == expected


def test_parse_hexchars_error():
    with pytest.raises(TypeError):
        deobfuscate.parse_hexchars('string')


def test_find_arrays_error():
    with pytest.raises(TypeError):
        deobfuscate.find_arrays('string')


@pytest.mark.parametrize(('unparsed', 'expected'), (
    (['var array = [1, 2, 3];', 'let d = array[1];'], 
     {'array': ['1', '2', '3']}), 
    (['let elts=[1];', 'var alist =[1,"2", 3];'],
     {'elts': ['1'], 'alist': ['1', '"2"', '3']}),
    (['const DOUG = [1, 2, 3, ["1", 2]]'],
     {'DOUG': ['1', '2', '3', ['"1"', '2']]})
    ))
def test_find_arrays(unparsed, expected):
    assert deobfuscate.find_arrays(unparsed) == expected

