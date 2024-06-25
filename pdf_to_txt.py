'''
filename: pdf_to_txt.py
'''

import pdfplumber # pip install pdfplumber

def pdf_convert(pdf, txt):
    '''convert pdf files to txt'''
    text = ''

    with pdfplumber.open(pdf) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    with open(txt, "w") as outfile:
        outfile.write(text)