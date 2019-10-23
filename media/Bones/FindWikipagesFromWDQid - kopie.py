# This is to find WP-articles and Commons cat for a given Wikidata Q-number
#
# 1 How to find target Wikipedia articles & Commons cats?
#
# Match images to Qids
# From the Qqids we can the WP-articles in all languages via urls like https://www.wikidata.org/w/api.php?action=wbgetentities&format=xml&props=sitelinks&ids=Q1979420%7CQ1424568&sitefilter=
# For Simple Wikipedia : https://www.wikidata.org/w/api.php?action=wbgetentities&format=xml&props=sitelinks&ids=Q1979420%7CQ1424568&sitefilter=simplewiki
# Via the API we can request the lenght of each article and how many images are included --> we can add the Smart images to articles that have a low/image word ratio (much text, few images is a target, and article with 0 images is a definte target.
#
# 2 How to find target Commons cats?
# Via WD P373

# Make a Excel file with 2 sheets
# 1 Suggested WP artielces, color-coded cells https://stackoverflow.com/questions/39299509/coloring-cells-in-excel-with-pandas
# 2 Suggested Commons cat
#=====================================================

import os, os.path
import pandas as pd
import urllib.request, json
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from collections import Counter

def getData(qid):
    if qid != 0:
        wdapiurl='https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&ids=' + str(qid)
        with urllib.request.urlopen(wdapiurl) as url:
            data = json.loads(url.read().decode())
        return data
    else:
        print("Qid = 0 - No data returned")
        return None

def getWikiIDs(qid):
    if qid != 0:
        data = getData(qid)
        if data:
            wiki_ids = data['entities'][qid]['sitelinks'].keys()
            if wiki_ids:
                print(wiki_ids)
                return wiki_ids
            else:
                print("No sitelinks for " + str(qid))
                return None
        else:
            print("No data returned for " + str(qid))
            return None
    else:
        print("Qid = 0 - No wiki_ids returned")
        return None

def getWikiBaseUrl(wiki_id):
    wiki_id2 = wiki_id.replace('_', '-')  # WP language 'bat_smg' vs 'bat-smg'
    #Wikipedia
    if wiki_id.endswith('wiki') and wiki_id != 'commonswiki':  # Wikipedia zh_classical[wiki] zea[wiki]
        wikibaseurl = 'https://' + str(wiki_id2)[:-4] + '.wikipedia.org/wiki/' 
    #Commons
    elif wiki_id == 'commonswiki':  # #wikimedia commons
        wikibaseurl = 'https://commons.wikimedia.org/wiki/' 
    #### Other Wikis
    elif wiki_id ==  'metawiki':
        wikibaseurl = 'https://meta.wikimedia.org/wiki/' 
    elif wiki_id.endswith('wikisource'): # Wikisource ca[wikisource]
        wikibaseurl = 'https://' + str(wiki_id2)[:-10] + '.wikisource.org/wiki/' 
    elif wiki_id.endswith('wikibooks'): #wikibooks tr[wikibooks]
        wikibaseurl = 'https://' + str(wiki_id2)[:-9]+ '.wikibooks.org/wiki/' 
    elif wiki_id.endswith('wikinews'): # wikinews
        wikibaseurl = 'https://' + str(wiki_id2)[:-8] + '.wikinews.org/wiki/'
    elif wiki_id.endswith('wikiquote'): # wikiquote zh[wikiquote]
        wikibaseurl = 'https://' + str(wiki_id2)[:-9] + '.wikiquote.org/wiki/' 
    elif wiki_id.endswith('wikiversity'): # Wikiversity en[wikiversity]
        wikibaseurl = 'https://' + str(wiki_id2)[:-11] + '.wikiversity.org/wiki/'
    elif wiki_id.endswith('wiktionary'):#  ar[wiktionary]
        wikibaseurl = 'https://' + str(wiki_id2)[:-4] + '.wiktionary.org/wiki/' 
    elif wiki_id.endswith('wikivoyage'):  # #wikivoyage
        wikibaseurl = 'https://' + str(wiki_id2)[:-10] + '.wikivoyage.org/wiki/'
    else: wikibaseurl ='WEEEERWATANDERS--AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    return wikibaseurl

# def findCommonsCatFromP373(qid):
#     # https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q48196 --> filter out value of P373 = Commons cat name
#     wdapiurl='https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=' + str(qid) + '&format=json'
#     with urllib.request.urlopen(wdapiurl) as url:
#         data = json.loads(url.read().decode())
#         if qid != 0:
#             if 'P373' in data['claims']:
#                 commonscatname = data['claims']['P373'][0]['mainsnak']['datavalue']['value'].replace(' ','_')
#                 commonscaturl = 'https://commons.wikimedia.org/wiki/Category:' + str(commonscatname)
#                 return commonscaturl
#             else:
#                 mes = "Qid != 0, but no P373-cat"
#                 print(mes)
#                 return mes
#         else: #qid=0
#             mes = "No P373-cat as Qid = 0"
#             print(mes)
#             return mes

def findWikipediaPages(qid):
    wikipedialist=[]
    if qid != 0:
        data = getData(qid)
        wiki_ids = getWikiIDs(qid)
        if data and wiki_ids: # there are data and sitelinks
            for id in wiki_ids:
                if id.endswith('wiki') and id != 'commonswiki': #Wikipedia pages only
                    baseurl = getWikiBaseUrl(id)
                    wptitle = data['entities'][qid]['sitelinks'][id]['title'].replace(' ','_')
                    wpurl= baseurl + wptitle
                    wikipedialist.append(wpurl)
            return wikipedialist
        else:
            print("Data or sitelinks missing")
            return None
    else:
        print("Qid = 0 - No Wikipedia pages returned")
        return None

# def findCommonsPages(qid):
#     wmcommonslist=[]
#     if qid != 0 :
#         getWikiIDs(qid)
#         if 'commonswiki' in wiki_ids: #there are sitelinks for WMC
#             getWikiBaseUrlFromID('commonswiki')
#             wiki_title = data['entities'][qid]['sitelinks']['commonswiki']['title'].replace(' ', '_')
#             wmcommonslist.append(getWikiBaseUrlFromID('commonswiki')+str(wiki_title))
#
#             if findCommonsCatFromP373(qid) == "Qid != 0, but no P373-cat":
#                print('No P377-based Commons cats to add')
#             else:
#                 if findCommonsCatFromP373(qid) != commonsurl: #Avoid the same caturl twice
#                     wmcommonslist.append(findCommonsCatFromP373(qid))
#             return wmcommonslist
#
#         elif findCommonsCatFromP373(qid) != "Qid != 0, but no P373-cat":  #No sitelinks, but WEL P273
#             wmcommonslist.append(findCommonsCatFromP373(qid))
#             return wmcommonslist
#         else:
#             print("No sitelinks AND no P373 value stated for " + str(qid))
#             return None
#     else: return print("Q qid is zero (non-existent) for this image")

#def findOtherWikiPagesFromSitelinks(qid):


# def findWikipagesFromQid(qid):
#     # https://stackoverflow.com/questions/37079989/how-to-get-wikipedia-page-from-wikidata-id
#     wdapiurl='https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&ids=' + str(qid)
#     wikipedialist=[]
#     wmcommonslist=[]
#     otherwikislist=[]
#     with urllib.request.urlopen(wdapiurl) as url:
#         data = json.loads(url.read().decode())
#         if qid != 0 :
#             wiki_ids = data['entities'][qid]['sitelinks'].keys()
#             if wiki_ids: #there are sitelinks
#                 for wiki_id in wiki_ids:
#                     #print(wiki_id)  # 'arwiki', 'commonswiki', 'dewiki', 'enwiki', 'svwiki', 'viwiki'
#                     wiki_id2 = wiki_id.replace('_', '-') # 'bat_smg' vs 'bat-smg'
#                     wiki_title = data['entities'][qid]['sitelinks'][wiki_id]['title'].replace(' ','_')
#                     #### Wikipedia
#                     if wiki_id.endswith('wiki') and wiki_id !='commonswiki': # Wikipedia zh_classical[wiki] zea[wiki]
#                         articleurl = 'https://' + str(wiki_id2)[:-4] + '.wikipedia.org/wiki/' + str(wiki_title)
#                         wikipedialist.append(articleurl)
#                     #### Commons
#                     elif wiki_id == 'commonswiki':  # #wikimedia commons
#                         articleurl = 'https://commons.wikimedia.org/wiki/' + str(wiki_title)
#                         wmcommonslist.append(articleurl)
#                         if findCommonsCatFromP373(qid) == "Qid is non-zero, but there is no P373-based Commons cat for this qid":
#                             print('No P377-based Commons cats to add')
#                         else:
#                             if findCommonsCatFromP373(qid) != articleurl:
#                                 wmcommonslist.append(findCommonsCatFromP373(qid))
#                     #### Other Wikis
#                     elif wiki_id ==  'metawiki':
#                         articleurl = 'https://meta.wikimedia.org/wiki/' + str(wiki_title)
#                         otherwikislist.append(articleurl)
#                     elif wiki_id.endswith('wikisource'): # Wikisource ca[wikisource]
#                         articleurl = 'https://' + str(wiki_id2)[:-10] + '.wikisource.org/wiki/' + str(wiki_title)
#                         otherwikislist.append(articleurl)
#                     elif wiki_id.endswith('wikibooks'): #wikibooks tr[wikibooks]
#                         articleurl = 'https://' + str(wiki_id2)[:-9]+ '.wikibooks.org/wiki/' + str(wiki_title)
#                         otherwikislist.append(articleurl)
#                     elif wiki_id.endswith('wikinews'): # wikinews
#                         articleurl = 'https://' + str(wiki_id2)[:-8] + '.wikinews.org/wiki/' + str(wiki_title)
#                         otherwikislist.append(articleurl)
#                     elif wiki_id.endswith('wikiquote'): # wikiquote zh[wikiquote]
#                         articleurl = 'https://' + str(wiki_id2)[:-9] + '.wikiquote.org/wiki/' + str(wiki_title)
#                         otherwikislist.append(articleurl)
#                     elif wiki_id.endswith('wikiversity'): # Wikiversity en[wikiversity]
#                         articleurl = 'https://' + str(wiki_id2)[:-11] + '.wikiversity.org/wiki/' + str(wiki_title)
#                         otherwikislist.append(articleurl)
#                     elif wiki_id.endswith('wiktionary'):#  ar[wiktionary]
#                         articleurl = 'https://' + str(wiki_id2)[:-4] + '.wiktionary.org/wiki/' + str(wiki_title)
#                         otherwikislist.append(articleurl)
#                     elif wiki_id.endswith('wikivoyage'):  # #wikivoyage
#                         articleurl = 'https://' + str(wiki_id2)[:-10] + '.wikivoyage.org/wiki/' + str(wiki_title)
#                         otherwikislist.append(articleurl)
#                     else: articleurl ='WEEEERWATANDERS--AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
#                 return wikipedialist, wmcommonslist, otherwikislist
#             elif findCommonsCatFromP373(qid) != "Qid is non-zero, but there is no P373-based Commons cat for this qid": #No sitelinks, but WEL P273
#                 wmcommonslist.append(findCommonsCatFromP373(qid))
#                 return wmcommonslist
#             else:
#                 print("No sitelinks AND no P373 value stated for " + str(qid))
#                 return None
#         else: return print("Q qid is zero (non-existent) for this image")


#=================== MAIN STUFF ===========================

currentdir = os.path.dirname(os.path.realpath(__file__))  # Path of this .py file

# Input file stuff
filename_in = "File_renamer - Bones.xlsx"
excelpath_in = currentdir + "\\" + filename_in
sheetname = "DecomposedCurrentFilePaths"
df = pd.read_excel(excelpath_in, sheet_name=sheetname, header=0)
df.fillna(0, inplace=True) #fill empty cells with 0
df2=df[['CommonsTitle', 'Qid']]

#Output stuff - Prepare Excel to be generated
filename_out = "UptakeSuggester - Bones.xlsx"
excelpath_out = currentdir + "\\" + filename_out

wb = xlsxwriter.Workbook(excelpath_out)
cell_format1 = wb.add_format()
cell_format2 = wb.add_format()
#ell_format.set_pattern(1)  # This is optional when using a solid fill.
cell_format1.set_bg_color('#C0C0C0') #First 4 columns are fixed, and have gray color

cell_format2.set_bg_color('lime') #this fill color must become depentdant on the image to word ratio in th WP-article


def getImageURLs(wpurl):

    wplang = wpurl.split('.')[0].split('//')[1]
    wptitle = wpurl.split('/wiki/')[1]

    #https://www.mediawiki.org/wiki/API: Images
    import requests
    S = requests.Session()
    URL = "https://" + str(wplang) + ".wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": wptitle,
        "prop": "images",
        "imlimit": 200
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA['query']['pages']
    #print(PAGES.items())
    imagelist=[]

    CATCH THE CASR FOR 0 images, for insrance in  https://ps.wikipedia.org/wiki/د_هډوکي_ماتېدل
    (via https://www.wikidata.org/wiki/Q68833)
    for k, v in PAGES.items():
        for img in v['images']:
            imagelist.append(img["title"].split(":")[1]) #strip off the File: , Bestand: , Datei etc parts
    return imagelist

print('*' *100)

# def image2WordRatio(wpurl):
#     return ratio
#
# def getColor(ratio):
#     return color

ws_wp = wb.add_worksheet('Wikipedia')
ws_wp.set_column('A:C', 30) #column width
ws_wp.set_column('D:D', 10)

wikipedialist = []
#commonslist=[]
#otherwikilist=[]

xrow = 0
totalimagelist = []  # this list will contain all images of all wparticles for all rows of the dataframe

for index, row in df2.head(50).iterrows():
    rowimagelist = []  # this list will contain all images of all wparticles for this row pof the dataframe
    print(row['CommonsTitle'], row['Qid'])

    wmctitle = row['CommonsTitle']
    wmcfileurl = 'https://commons.wikimedia.org/wiki/File:' + str(wmctitle)
    qid = row['Qid']
    wdqurl = 'https://www.wikidata.org/wiki/' + str(qid)

    wikipedialist = findWikipediaPages(qid)
    if wikipedialist: #wplist != None
        print("Wikipedia list = " + str(wikipedialist))
        #https://xlsxwriter.readthedocs.io/tutorial01.html

        #Fill columns 0 (A) and 1 (B)  with File: name + url
        cell_0 = xl_rowcol_to_cell(xrow, 0)
        cell_1 = xl_rowcol_to_cell(xrow, 1)
        ws_wp.write(cell_0, wmcfileurl)
        ws_wp.write_formula(cell_1, '=HYPERLINK('+ cell_0+',"'+wmctitle+'")',cell_format1)

        #Fill columns 2 (C) and 3 (D) with WD-QID + url
        cell_2 = xl_rowcol_to_cell(xrow, 2)
        cell_3 = xl_rowcol_to_cell(xrow, 3)
        ws_wp.write(cell_2, wdqurl)
        ws_wp.write_formula(cell_3, '=HYPERLINK('+ cell_2+',"'+qid+'")',cell_format1)

        #Fill further (=E and further) columns with WP-list values
        for wpurl in wikipedialist:

            # cell_format.set_bg_color(color) #this fill color must become depentdant on the image to word ratio in th WP-article

            wplang = wpurl.split('.')[0].split('//')[1]
            #print(wplang)
            wptitle = wpurl.split('/wiki/')[1]
            #print(wptitle)
            wpclick=wplang+":"+wptitle #ca:Fractura_de_clavícula
            #print(wpclick)

            xcol = 2*(int(wikipedialist.index(wpurl))+2) #From wikipedialist index = 0,1,2,3 --> (even) cell index = 4,6,8,10
            #print(xrow, xcol)
            odd_cell = xl_rowcol_to_cell(xrow, xcol) # 'odd' cells = Ei,Gi,Ii,Ki; i=1,2,3,4,5,6
            ws_wp.write(odd_cell, wpurl)
            even_cell = xl_rowcol_to_cell(xrow, xcol+1) # 'even' cells = Fi,Hi,Ji,Li; i=1,2,3,4,5,6
            #print(even_cell)
            ws_wp.write_formula(even_cell, '=HYPERLINK('+odd_cell+',"'+ str(wpclick)+'")',cell_format2) #in alle even celindexen (

            imagelist=getImageURLs(wpurl)
            print("imagelist for " + str(wpurl) + " : " +  str(imagelist))
            rowimagelist.append(imagelist)
        flatrowimagelist = [item for sublist in rowimagelist for item in sublist] #flatten this listr of lists
        # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        print("flatrowimagelist : " + str(flatrowimagelist))
        crow = Counter(flatrowimagelist)  # counter generating code
        print("flatrowimagelist most common: " + str(crow.most_common()))
        totalimagelist.append(flatrowimagelist)
    xrow += 1
    print('*' * 100)

flattotalimagelist = [item for sublist in totalimagelist for item in sublist] #flatten this listr of lists
print("flattotalimagelist: " + str(flattotalimagelist))

#determine which images occur most often
#https://docs.python.org/2/library/collections.html#collections.Counter.most_common
ctotal = Counter(flattotalimagelist)  # counter generating code
mostcommonlist = ctotal.most_common()
print("flattotalimagelist most common: " + str(mostcommonlist))
print(' ' * 100)
print("===List of most common media files, and their no. of occurences===")
[print(str(tuple[0]) + " : "+ str(tuple[1])) for tuple in mostcommonlist]

wb.close()





