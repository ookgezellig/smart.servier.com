#Create content for https://commons.wikimedia.org/wiki/SMART-Servier_Medical_Clip_Art

import os, os.path
import pandas as pd

def findImages(dataframe,filedir):
#input: Folder (FileDir):
# output: images in that folder, formatted as English language Commons gallery
#   <gallery style="text-align:left">
#      File:Upper arm bone fracture - Humerus fracture 1 -- Smart-Servier.png|Humerus fracture
#      File:Upper arm bone fracture - Humerus fracture 2 -- Smart-Servier.png|Humerus fracture
#      File:Upper arm bone fracture - Humerus fracture -- Smart-Servier.jpg|Humerus fracture
#   </gallery>
    imageGallery = '<gallery style="text-align:left">\n'
    for index, row in dataframe.iterrows():
         if row["FileDir"] == filedir:
            imageGallery += 'File:' + row["CommonsTitle"] + '|' + row['CommonsFiledesc_EN'] + '\n'
    imageGallery += '</gallery>'
    return print(imageGallery)

def servierLookup(df,subdir):
    for index, row in df.iterrows():
        if row["SubDir"] == subdir:
            ssppt = row["ServierPPT"]
            ssurl = row["ServierWebsite"]
            ssflickr = row["ServierFlickr"]
    return ssppt, ssurl, ssflickr

def writeSubdirHeader(dataframe,subdir):
    #Example (for Bones // Bone fractures)
    # * ''Wikimedia Commons'': See [[:Category:SMART-Servier Medical Art - Bone fractures]]. Download the [[:File:Bones - Bone fractures -- Smart-Servier.pdf|original PDF]] and the [[:File:Bones - Bone fractures - White background -- Smart-Servier.pdf|PDF with white background]] for easier reuse.
    # * ''Smart Servier website'': [https://smart.servier.com/category/anatomy-and-the-human-body/locomotor-system/bones/ Images related to Bone fractures and Bones] -- [https://smart.servier.com/wp-content/uploads/2016/10/Bone_fractures.ppt Download in Powerpoint format].
    # * ''Flickr'': [https://www.flickr.com/photos/serviermedicalart/sets/72157635535468962 Images related to Bone fractures and Bones] (in French).
    subdirHeaderText = subdirHeaderTemplate.format(
        subdir = subdir,
        basedir = dataframe.BaseDir.unique()[0],
        ssppt = servierLookup(dataframe,subdir)[0],
        ssurl = servierLookup(dataframe,subdir)[1],
        ssflickr = servierLookup(dataframe,subdir)[2]
        )
    return subdirHeaderText

subdirHeaderTemplate = """
* ''Wikimedia Commons'': See [[:Category:SMART-Servier Medical Art - {subdir}]]. Download the [[:File:{basedir} - {subdir} -- Smart-Servier.pdf|original PDF]] and the [[:File:{basedir} - {subdir} - White background -- Smart-Servier.pdf|PDF with white background]] for easier reuse.
* ''Smart Servier website'': [{ssurl} Images related to {subdir} and {basedir}] -- [https://smart.servier.com/wp-content/uploads/2016/10/{ssppt} Download in Powerpoint format].
* ''Flickr'': [{ssflickr} Images related to {subdir}] (in French).
"""

#config paths/ urls
currentdir = os.path.dirname(os.path.realpath(__file__))  # Path of this .py file
filename = "File_renamer - Bones.xlsx"
excelpath = currentdir + "\\" + filename
sheetname = "DecomposedCurrentFilePaths"
df = pd.read_excel(excelpath, sheet_name=sheetname, header=0)
df.fillna(0, inplace=True) #fill empty cells with 0

df2=df[['BaseDir', 'SubDir', 'FileDir','CommonsTitle','CommonsFiledesc_EN','ServierPPT','ServierWebsite','ServierFlickr']]

uniqueBaseDir = df2.BaseDir.unique()
#print(uniqueBaseDir)
uniqueSubDir = df2.SubDir.unique()
#print(uniqueSubDir)
uniqueFileDir = df2.FileDir.unique()
#print(uniqueFileDir)

#for i in range(200,len(df)):
for ubd in uniqueBaseDir:
    print('=' + str(ubd) + '=')
    for usd in uniqueSubDir:
        print('==' + str(usd) + '==')
        print(writeSubdirHeader(df2, usd))
        for ufd in uniqueFileDir:
            if usd in ufd:
                print('===' + str(ufd) + '===')
                findImages(df2, ufd)

