# This is input for <FileUpload.py> that actually writes the content to Wikimedia commons using the API
#See https://pypi.org/project/mwtemplates/

def findRelatedImages(dataframe,commonstitle):
#input: Commons image file in folder (FileDir): File:Upper arm bone fracture - Humerus fracture -- Smart-Servier.jpg
#output: other images in the same folder, formatted as English language Commons gallery
#   <gallery style="text-align:left">
#      File:Upper arm bone fracture - Humerus fracture 1 -- Smart-Servier.png|Humerus fracture
#      File:Upper arm bone fracture - Humerus fracture 2 -- Smart-Servier.png|Humerus fracture
#   </gallery>
    relatedImagesGallery = '<gallery style="text-align:left">\n'
    for index, row in dataframe.iterrows():
        if row["CommonsTitle"] == commonstitle:
            filedir = row["FileDir"]
            for index, row in dataframe.iterrows():
                if row["FileDir"] == filedir:
                    if row["CommonsTitle"] != commonstitle:
                        relatedImagesGallery += 'File:' + row["CommonsTitle"] + '|' + descriptionENlookup(dataframe, row["CommonsTitle"]) + '\n'
                        # For next batch Check if THIS WORKS:
                        # relatedImagesGallery += 'File:' + row["CommonsTitle"] + '|' + row["CommonsFiledesc_EN"] + '\n'
                        #And then delete the def descriptionENlookup below
    relatedImagesGallery += '</gallery>'
    return relatedImagesGallery

def descriptionENlookup(dataframe,commonstitle):
# Lookup English image description for a given Commons title in Excel sheet
# eg 'Thigh bone fracture - Fracture of femur 6 -- Smart-Servier.png' --> 'Thigh bone fracture - Fracture of femur'
# in File_renamer - Bones.xlsx/DecomposedCurrentFilePaths
    # https://www.interviewqs.com/ddi_code_snippets/iterate_rows_pandas
    for index, row in dataframe.iterrows():
        if row["CommonsTitle"] == commonstitle:
            descriptionEN = row["CommonsFiledesc_EN"]
    return descriptionEN

from datetime import date
today = date.today()

# ===============BEGIN TEMPLETE======================
# Lets'try to base it on the {{Artwork}} template - https://commons.wikimedia.org/wiki/Template:Artwork
fileTemplate = """
=={{{{int:filedesc}}}}==
{{{{Artwork
 |author             = {{{{Institution:Laboratoires Servier}}}}
 |title              = 
 |description        = {{{{en|1={descrEN}}}}} {{{{fr|1={descrFR}}}}} {{{{nl|1={descrNL}}}}} {{{{sv|1={descrSV}}}}}
 |date               = {currentdate}
 |institution        =
 |notes              =
 |source             = * ''Smart Servier website'': [{ssurl} Images related to {medicalname}{commonname}, {categoryEN} and {basedir}] -- [https://smart.servier.com/wp-content/uploads/2016/10/{ssppt} Download in Powerpoint format].
* ''Flickr'': [{ssflickr} Images related to {medicalname}{commonname} and {categoryEN}] (in French).
 |permission         =
 |other_versions     =  Related images {relatedimagesgallery}
 |references         =
 |wikidata           = {wikidataqid}
}}}}

=={{{{int:license-header}}}}==
{{{{SMART-Servier_Medical_Art}}}}
{{{{Cc-by-sa-3.0}}}}

[[Category:SMART-Servier Medical Art - {cat}]]
"""
# ==============END TEMPLATE====================
def writeFileTemplate(dataframe,rowdict): # input = 1 full row from the Excel sheet, formatted as dict
    # Input = 1 row from Excel file, as dict
    # Ouput = Commons source code for a file page, based on Artwork-template

    fileText = fileTemplate.format(
    #Descriptions in multiple languages
    descrEN =  rowdict['Category_EN'].strip() + ' - ' + rowdict['CommonsFiledesc_EN'].strip(),
    descrFR =  rowdict['Category_FR'].strip() + ' - ' + rowdict['CommonsFiledesc_FR'].strip(),
    descrNL =  rowdict['Category_NL'].strip() + ' - ' + rowdict['CommonsFiledesc_NL'].strip(),
    descrSV =  rowdict['Category_SV'].strip() + ' - ' + rowdict['CommonsFiledesc_SV'].strip(),
    currentdate = today.strftimeDITFORMAATAANPASSEN - JAREKT("%d %B %Y"), # MOET WORDEN; 2019-09-29
    medicalname = rowdict['MedicalName'].strip(),
    commonname = ' (' + rowdict['CommonName'].strip() + ')' if rowdict['CommonName'] != 0 else '', #https://recalll.co/ask/v/topic/Python-conditional-string-formatting/5a12013c1126f4f8418b7aae
    categoryEN = rowdict['Category_EN'].strip(),
    #basedir = rowdict['BaseDir'].strip(),
    #External links
    ssppt = rowdict['ServierPPT'].strip(),
    ssurl = rowdict['ServierWebsite'].strip(),
    ssflickr = rowdict['ServierFlickr'].strip(),
    wikidataqid = '' if  rowdict['Qid'] == 0 else rowdict['Qid'],
    # related images
    relatedimagesgallery = findRelatedImages(dataframe,rowdict['CommonsTitle']),
    #CommonsCat
    cat = rowdict['SubDir']
    )
    return fileText