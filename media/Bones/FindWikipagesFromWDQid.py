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

api_url = 'https://commons.wikimedia.org/w/api.php'

currentdir = os.path.dirname(os.path.realpath(__file__))  # Path of this .py file
filename = "File_renamer - Bones.xlsx"
excelpath = currentdir + "\\" + filename
sheetname = "DecomposedCurrentFilePaths"
df = pd.read_excel(excelpath, sheet_name=sheetname, header=0)
df.fillna(0, inplace=True) #fill empty cells with 0

df2=df[['CommonsTitle', 'Qid']]
dfdict=df2.to_dict(orient='records')

def findWikipagesFromQid(qid):
    # https://stackoverflow.com/questions/37079989/how-to-get-wikipedia-page-from-wikidata-id
    wdapiurl='https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&ids=' + str(qid)
    with urllib.request.urlopen(wdapiurl) as url:
        data = json.loads(url.read().decode())
        wiki_ids = data['entities'][qid]['sitelinks'].keys()
        for wiki_id in wiki_ids:
            print(wiki_id)  # 'arwiki', 'commonswiki', 'dewiki', 'enwiki', 'svwiki', 'viwiki'
            wiki_id2 = wiki_id.replace('_', '-') # 'bat_smg' vs 'bat-smg'
            wiki_title = data['entities'][qid]['sitelinks'][wiki_id]['title'].replace(' ','_')

            if wiki_id == 'commonswiki': # #wikimedia commons
                articleurl = 'https://commons.wikimedia.org/wiki/' + str(wiki_title)
            elif wiki_id ==  'metawiki':
                articleurl = 'https://meta.wikimedia.org/wiki/' + str(wiki_title)
            elif wiki_id.endswith('wiki'): # Wikipedia zh_classical[wiki] zea[wiki]
                articleurl = 'https://' + str(wiki_id2)[:-4] + '.wikipedia.org/wiki/' + str(wiki_title)
            elif wiki_id.endswith('wikisource'): # Wikisource ca[wikisource]
                articleurl = 'https://' + str(wiki_id2)[:-10] + '.wikisource.org/wiki/' + str(wiki_title)
            elif wiki_id.endswith('wikibooks'): #wikibooks trwikibooks
                articleurl = 'https://' + str(wiki_id2)[:-9]+ '.wikibooks.org/wiki/' + str(wiki_title)
            elif wiki_id.endswith('wikinews'): # wikinews
                articleurl = 'https://' + str(wiki_id2)[:-8] + '.wikinews.org/wiki/' + str(wiki_title)
            elif wiki_id.endswith('wikiquote'): # wikiquote zh[wikiquote]
                articleurl = 'https://' + str(wiki_id2)[:-9] + '.wikiquote.org/wiki/' + str(wiki_title)
            elif wiki_id.endswith('wikiversity'): # Wikiversity en[wikiversity]
                articleurl = 'https://' + str(wiki_id2)[:-11] + '.wikiversity.org/wiki/' + str(wiki_title)
            elif wiki_id.endswith('wiktionary'):#  ar[wiktionary]
                articleurl = 'https://' + str(wiki_id2)[:-4] + '.wiktionary.org/wiki/' + str(wiki_title)
            elif wiki_id.endswith('wikivoyage'):  #        #wikivoyage
                articleurl = 'https://' + str(wiki_id2)[:-10] + '.wikivoyage.org/wiki/' + str(wiki_title)
            else:
                articleurl ='WEEEERWATANDERS--AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
            print(articleurl)
        #print(data['entities'][qid]['sitelinks'].values())
    return print(id)


for i in range(0,1):
#for i in range(100,200):
#for i in range(200,len(df)):
    rowdict = dfdict[i]
    #print(rowdict)
    #findWParticlesFromQid(rowdict['Qid'])
    findWikipagesFromQid('Q90')


    #descriptionEN = descriptionENlookup(df,rowdict['CommonsTitle'])
    #print(rowdict['CommonsTitle'] + " --> " + descriptionEN)
    #findRelatedImages(df,rowdict['CommonsTitle'])


#Check if "site":"commonswiki","title":"Category:Human vertebral column","badges":[]} from  WD-api call is the same as WD P373

