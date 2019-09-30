# Rename jpg and png files in folders
#Bone fractures
#Bone structure
#Skeleton and bones

import os, os.path, glob
import xlrd


#config paths/ urls
currentdir = os.path.dirname(os.path.realpath(__file__)) # Path of this .py file
# basedir= "Bones" # Change this according to the targeted base folder
# subdir = "Skeleton and bones" # Change this according to the targeted subfolder
# homedir= currentdir + "\\" + basedir + "\\" + subdir + "\\"

excelpath= currentdir  + "\\" + "File_renamer - Bones.xlsx"
#print(excelpath)


# Read from Excel https://www.codespeedy.com/reading-an-excel-sheet-using-xlrd-module-in-python/
#https://blogs.harvard.edu/rprasad/2014/06/16/reading-excel-with-python-xlrd/

# Give the address of the file on the local computer, i.e, path location
# To open Workbook we declare a hadling variable wb
xl_workbook = xlrd.open_workbook(excelpath)
sheet_names = xl_workbook.sheet_names()
#print('All sheets in this workbook: ', sheet_names)

xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
#print ('First sheet name: %s' % xl_sheet.name)

# row = xl_sheet.row(0)  # 1st row
# # Print 1st row values and types
# from xlrd.sheet import ctype_text
# print('(Column #) type:value')

for i in range(1, xl_sheet.nrows): # This worls hor all!
#for i in range(1, 5): # First 2 rows
    #https://www.blog.pythonlibrary.org/2014/04/30/reading-excel-spreadsheets-with-python-and-xlrd/
    rowslice = xl_sheet.row_slice(rowx=i,start_colx=0,end_colx=2) # List of first 3 cells in row 1

    current_full_filepath = str(rowslice[0])[6:-1]
    #http://xahlee.info/python/python_path_manipulation.html
    #basepath = os.path.split(current_full_filepath)[0]
    #current_filename = str(rowslice[1])[6:-1]
    #new_filename = str(rowslice[2])[6:-1]
    #new_full_filepath = basepath + "\\" + new_filename
    new_full_filepath  = str(rowslice[1])[6:-1]

    #print("Current full filepath (from Excel file): " + current_full_filepath)
    print(current_full_filepath)
    #print("Basepath: "+ basepath)
    #print("Current filename (from Excel file): "  + current_filename)
    #print("New filename(from Excel file): " + new_filename )
    #print("New full filepath: " + new_full_filepath)
    print(new_full_filepath)

    # Check if New full filepath is the same at the Current full filepath : if so. do not rename. If not, then do rename
    print ('*'*40)
    if current_full_filepath == new_full_filepath:
        print("New filename (and full path) IS THE SAME AS current filename (and full path), no need to rename")
    else:
        print("New filename (and full path) IS BETTER  THAN current filename (and full path), we are going to rename!")
        os.rename(current_full_filepath, new_full_filepath)

