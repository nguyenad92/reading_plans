import os
import sys

from pdf2image import convert_from_path 
from PIL import Image

import pytesseract
from pytesseract import Output
import re
import PyPDF2

import tabula

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
    pdf_object = open(THIS_FOLDER + '/Plans/' + filename, 'rb')  #Open the file

                  

    pdf = PyPDF2.PdfFileReader(pdf_object)                       #read pdf file
    
    total_page = pdf.numPages                                   #get total page of the file
    # print('File ' + str(count) + ' has ' + str(total_page))
    # count += 1
    print(rename)
    print('Total page is: ' + str(total_page))

    if total_page < 200:

        # Testing specific page
        # page_object = pdf.getPage(22)
        # text = page_object.extractText()
        # # print(text)
        # if keywords in text:
        #     print('found it')

        for page in range(total_page):
            page_object = pdf.getPage(page)
            text = page_object.extractText()

            # print(page)
            # if page == 76:
            #     tabula.convert_into(THIS_FOLDER + '/Plans/' + filename, THIS_FOLDER + '/Tables/' + rename + '-page_' + str(page + 1) + '.csv', output_format='csv', pages=page+1)
           
            # if text == '':
            #     print('text is empty in page ' + str(page))
            #     # page_test = convert_from_path(pdf.getPage(page))
            #     # PDF page n -> page_n.jpg 
            #     image_page = convert_from_path(THIS_FOLDER + '/Plans/' + filename, first_page=page, last_page=page)
            #     image_name = "page_"+str(page)+".jpg"
                
            #     # Save the image of the page in system 
            #     image_page[0].save(THIS_FOLDER + '/Plan Images/' + rename + image_name, 'JPEG') 
            #     text = str(((pytesseract.image_to_string(Image.open(THIS_FOLDER + '/Plan Images/' + rename + image_name)))))
                # print(text)

            # To test which page used PyPDF2
            # else:
            #     print('text found in page ' + str(page))
            
            # print(text)

            # for i in keywords:
            #     if re.search(r'\b{}\b'.format(i), text):
            #         print('found window schedule of' + filename + ' in page ' + str(page + 1))

            if keywords in text.lower():
                print('found window schedule of ' + filename + ' in page ' + str(page + 1))
                output_page = PyPDF2.PdfFileWriter()
                output_page.addPage(page_object)
                with open(THIS_FOLDER + '/Window Schedule/' + rename + '-page_' + str(page + 1) + '.pdf', 'wb') as outputStream:
                    output_page.write(outputStream)

                # table = tabula.read_pdf(filename, pages=page)
                tabula.convert_into(THIS_FOLDER + '/Plans/' + filename, THIS_FOLDER + '/Tables/' + rename + '-page_' + str(page + 1) + '.csv', output_format='csv', pages=page+1)
                


        
    
    
    # print(entry)