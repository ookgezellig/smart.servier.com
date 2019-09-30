# Aim - extract French texts from png files# We need to convert the transparent pngs to non-transparent ones


from PIL import Image
import pytesseract
import os, os.path, glob
import xlrd


#config paths/ urls
currentdir = os.path.dirname(os.path.realpath(__file__)) # Path of this .py file

excelpath= currentdir  + "\\" + "File_renamer - Bones.xlsx"
print(excelpath)

# Read from Excel https://www.codespeedy.com/reading-an-excel-sheet-using-xlrd-module-in-python/
#https://blogs.harvard.edu/rprasad/2014/06/16/reading-excel-with-python-xlrd/

# Give the address of the file on the local computer, i.e, path location
# To open Workbook we declare a hadling variable wb
xl_workbook = xlrd.open_workbook(excelpath)
sheet_names = xl_workbook.sheet_names()
#print('All sheets in this workbook: ', sheet_names)

xl_sheet = xl_workbook.sheet_by_name(sheet_names[1])
print ('First sheet name: %s' % xl_sheet.name)
print(xl_sheet.nrows)

for i in range(1, xl_sheet.nrows): # This worls hor all!
#for i in range(1, 5): # First 2 rows
    #https://www.blog.pythonlibrary.org/2014/04/30/reading-excel-spreadsheets-with-python-and-xlrd/
    rowslice1 = xl_sheet.row_slice(rowx=i,start_colx=0,end_colx=1)
    rowslice2 = xl_sheet.row_slice(rowx=i, start_colx=3, end_colx=4)
    full_filepath = rowslice1[0].value + rowslice2[0].value


    #We need to convert all tranparent png to jpg with black bakgrounsd
    if rowslice2[0].value == '.png':
        image=Image.open(full_filepath)
        non_transparent=Image.new('RGB',image.size,(0,0,0))
        non_transparent.paste(image,(0,0),image)
        #non_transparent.show()

        # Include tesseract executable in your path
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        image_to_text = "a"

        # Create an image object of PIL library
        #image = Image.open(non_transparent)

        # pass image into pytesseract module, pytesseract is trained in many languages
        image_to_text = pytesseract.image_to_string(non_transparent, lang='eng')
        image.close()
        # Print the text
        print(full_filepath + "^^" + ' '.join(image_to_text.split()))
        #print(image_to_text)
    else:print(full_filepath + "^^" + "JPG detected")