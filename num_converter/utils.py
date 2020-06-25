import re

def _remove_gaps_in_number(line):
    #remove gaps inside of the number
    cline = re.sub('(?<=[\d])[\D]+(?=[\d]{1,8}(\D|$))', '', line)

    return cline

def _normalize_numbers(numbers):
    res = set()
    for number in numbers:
        res.add("370"+number)

    return res

def _extract_numbers(line):
    #6+digit*7
    numbers = re.findall("6[\d]{7}(?=\D|$)", line)

    return _normalize_numbers(numbers)

def convert(lines):

    conv_numbers = set()
    for line in lines:

        cline = _remove_gaps_in_number(line)

        new_nums = _extract_numbers(cline)
        conv_numbers |= new_nums

    return conv_numbers