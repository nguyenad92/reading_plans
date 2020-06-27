import os
import sys

from pdf2image import convert_from_path 
from PIL import Image

import pytesseract
from pytesseract import Output
import re
import PyPDF2

import tabula

# using pdfminer.six
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# import textract

# import pdfplumber
# import json


    

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

folder_name = 'Plans'
output_folder_name = 'Plan Images'
try:
    folder = os.listdir(folder_name)
except:
    print('There is no Plans folder')
# print(folder)

# keywords = ['WINDOW SCHEDULE', 'W I N D O W S C H E D U L E']
# keywords = 'WINDOW SCHEDULE'
keywords = 'window schedule'


# output = open('out.txt', 'a')


for filename in folder:
    # filename = os.path.join(THIS_FOLDER, entry)
    rename = filename.strip('.pdf')
    path = THIS_FOLDER + '/Plans/' + filename
    pdf_object = open(path, 'rb')  #Open the file

    pdf = PyPDF2.PdfFileReader(pdf_object)                       #read pdf file
    
    total_page = pdf.numPages 
    count = 0

    with open(path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        for page in PDFPage.create_pages(doc):
            output_string = StringIO()
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # creat a single page ofject using pdf2image
            page_object = pdf.getPage(count)
            count += 1

            print(count)
            interpreter.process_page(page)
            text = output_string.getvalue()
            text = text.lower()
            if 'window' in text.lower() and 'schedule' in text.lower() and 'type' in text.lower() and 'index' not in text.lower() and ('glazing' in text.lower() or 'width' in text.lower() or 'size' in text.lower()):
                print('found')
                print(count)
                output_page = PyPDF2.PdfFileWriter()
                output_page.addPage(page_object)
                with open(THIS_FOLDER + '/Window Schedule/' + rename + '-page_' + str(count) + '.pdf', 'wb') as outputStream:
                    output_page.write(outputStream)

                # table = tabula.read_pdf(filename, pages=page)
                tabula.convert_into(THIS_FOLDER + '/Plans/' + filename, THIS_FOLDER + '/Tables/' + rename + '-page_' + str(count) + '.csv', output_format='csv', pages=count+1)
          
            text = ''
            output_string.close()


            

    # print(output_string.getvalue())
    # retstr = StringIO()
    # parser = PDFParser(open('/Plans/' + filename,'r'))

    
    # document = PDFDocument(parser)
  
    # if document.is_extractable:
    #     rsrcmgr = PDFResourceManager()
    #     device = TextConverter(rsrcmgr,retstr, codec='ascii' , laparams = LAParams())
    #     interpreter = PDFPageInterpreter(rsrcmgr, device)
    #     for page in PDFPage.create_pages(document):
    #         interpreter.process_page(page)
    # else:
    #     print(path,"Warning: could not extract text from pdf file.")

    # text = retstr

    #             # table = tabula.read_pdf(filename, pages=page)
    #             tabula.convert_into(THIS_FOLDER + '/Plans/' + filename, THIS_FOLDER + '/Tables/' + rename + '-page_' + str(page + 1) + '.csv', output_format='csv', pages=page+1)
                


        
    
    
