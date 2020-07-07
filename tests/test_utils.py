import pytest

from num_converter import utils

@pytest.mark.parametrize(("line", "cline", "passs"),
    [
        ("861002203", "861002203", True),
        ("8 61002203", "861002203", True),
        ("8@61002203", "861002203", True),
        ("8 6 1002203", "861002203", True),
        ("8 6 1 0 0 2 2 0 3", "861002203", True),
        ("86  1002203", "861002203", True),
        ("86 100220 3", "861002203", True),
        (" 861002203", " 861002203", True),
        (" 861002203 ", " 861002203 ", True),
        (" 86 1002203", " 861002203", True),
        ("86 1002203 ", "861002203 ", True),
        ("+370 6 1002203", "+37061002203", True),
        ("+37061002203", "+37061002203", True),
        ("3706 1002203", "37061002203", True),
        ("6 1002203", "61002203", True),
        ("61002203", "61002203", True),
        ("86,1002203", "861002203", True),
        ("861002203 861002203", "861002203 861002203", True),
        ("86 1002203 861002203", "861002203 861002203", True),
        ("86 1002203 86 1002203", "861002203 861002203", False),
        ("86 1002203 861002203", "861002203 861002203", True),
        ("8 6100 22 03 +37061002203", "861002203 +37061002203", True),
        ("8 6100 2203 37061002203", "861002203 37061002203", True),
        ("8 6100 2203 +370 61002203", "861002203 +37061002203", False),
        ("8 6100 22 03 +370 6 1002203", "861002203 +37061002203", False),
        ("8 6100 22 03 370 6 1002203", "861002203 37061002203", False),
        ("861002203;+37061002203", "861002203;+37061002203", True),
        ("86 1002203;+37061002203", "861002203;+37061002203", True),
        ("8 6100 22 03;+37061002203", "861002203;+37061002203", True),
        ("8 6100 2203;37061002203", "861002203;37061002203", True),
        ("8 6100 2203;+370 61002203", "861002203;+37061002203", False),
        ("8 6100 22 03;+370 6 1002203", "861002203;+37061002203", False),
        ("8 6100 22 03;370 6 1002203", "861002203;370 6 1002203", False)
    ])
def test_remove_gaps(line, cline, passs):
    res = utils._remove_gaps_in_number(line)

    if passs:
        assert res == cline
    else:
        assert res != cline

@pytest.mark.parametrize(("numbers", "results"),
    [
        ( ["61002203"], set(["37061002203"]) ),
        ( ["61002203", "61002202"], set(["37061002203", "37061002202"]) ),
        ( ["61002203", "61002203"], set(["37061002203"]) )
    ])
def test_normalize_numbers(numbers, results):
    res = utils._normalize_numbers(numbers)

    assert res == results

@pytest.mark.parametrize(("line", "numbers"),
    [
        ("61002203", set(["37061002203"])),
        (" 61002203", set(["37061002203"])),
        ("61002203 ", set(["37061002203"])),
        (" 61002203 ", set(["37061002203"])),
        ("@x61002203xx", set(["37061002203"])),
        ("+37061002203", set(["37061002203"])),
        ("861002203", set(["37061002203"])),
        ("861002203 ", set(["37061002203"])),
        ("861002203 861002203", set(["37061002203", "37061002203"])),
        ("861002203 +37061002203;61002203", set(["37061002203", "37061002203", "37061002203"]))
    ])
def test_extract_numbers(line, numbers):

    res = utils._extract_numbers(line)

    assert res == numbers

@pytest.mark.parametrize(("lines", "results"),
    [
        ( ["861002202", "861002203"], set(["37061002202", "37061002203"]) ),
        ( ["861002201 +37061002202", "861002203"], set(["37061002201", "37061002202", "37061002203"]) )
    ])
def test_convert(lines, results):

    res = utils.convert(lines)

    assert res == results