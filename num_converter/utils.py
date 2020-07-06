import re

import pandas
import textract
import docx

#Clean up numbers
def _remove_gaps_in_number(line):
    #remove gaps inside of the number
    try:
        cline = re.sub('(?<=[\d])[\D]+(?=[\d]{1,8}(\D|$))', '', line)
    except e:
        print(e)

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


#Read TXT
def read_txt(filepath):
    lines = []
    with open(filepath, 'r') as file1:
        lines = file1.readlines()

    return lines


#Read XLSX/XLS
def read_excel(filepath):
    cells = set()
    xl = pandas.read_excel(filepath, sheet_name=None)

    for sheet_name in xl:
        cells |= { str(cell) for cell in xl[sheet_name].values.flatten() if cell==cell}

    return cells

#Read DOCX
#DOC also possible but would need apt-install antiword..
def read_word(filepath):
    text = textract.process(filepath)
    lines = text.decode('utf-8').split('\n\n')

    return lines

#Write TXT
def write_txt(ofilepath, content):
    with open(ofilepath, 'w') as ofile:
        for number in content:
            ofile.write("%s\n" % number)

#Write EXCEL
def write_excel(ofilepath, content):
    df = pandas.DataFrame(list(content))
    writer = pandas.ExcelWriter(ofilepath, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', header=False, index=False)

    writer.save()

#Write WORD
def write_word(ofilepath, content):
    document = docx.Document()
    for number in content:
        document.add_paragraph(number)

    document.save(ofilepath)
