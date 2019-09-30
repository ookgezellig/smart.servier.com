

#Login to the MediaWiki API to write categories to Commons - Code from https://www.mediawiki.org/wiki/API:Edit/Editing_with_Python




#for loop over alle 600+ boeken (ook niet PD)
pd_counter = 0

for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):

    title=""
    summary=""
    glamorous=""
    message=""

    ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:recordIdentifier")  # PRB01:175094691
    #print("ppn_long: "+ ppn_long)
    ppn = ppn_long.split(":")[1]  # 175094691 #length is always 9 chars
    if ppn in catsdata.keys():
        pd_counter += 1
        commonsHomeCat=catsdata[ppn]["HomeCat"] # See http://stackoverflow.com/questions/17322668/typeerror-dict-keys-object-does-not-support   -indexing

        commonsHomeCat_trunc = commonsHomeCat.split(":")[1] #take the part after 'Category:'
        sorter=""
        if commonsHomeCat_trunc.startswith("De "): #Starting with "De "
            sorter = commonsHomeCat_trunc[3:]
        if commonsHomeCat_trunc.startswith("Het "):#Starting with "Het "
            sorter = commonsHomeCat_trunc[4:]
        if commonsHomeCat_trunc.startswith("Een "):#Starting with "Een "
            sorter = commonsHomeCat_trunc[4:]
        #print(sorter)

        # Write parent categories ==
        ## Default parent cats
        parentcats = ""
        if sorter != "":
            parentcats += '[[Category:Picture books from Koninklijke Bibliotheek|' + sorter + ']]\n'
        else:
            parentcats += '[[Category:Picture books from Koninklijke Bibliotheek]]\n'

        ## Optional parent cats
        if "SubjectCats" in catsdata[ppn]:
            commonsSubjectCat = catsdata[ppn]["SubjectCats"]
            if sorter != "":
                parentcats += '[[' + commonsSubjectCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsSubjectCat + ']]\n'

        if "AnnotationCats" in catsdata[ppn]:
            commonsAnnotationCat = catsdata[ppn]["AnnotationCats"]
            if sorter != "":
                parentcats += '[[' + commonsAnnotationCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsAnnotationCat + ']]\n'

        if "AuteurCats" in catsdata[ppn]:
            commonsAuteurCat = catsdata[ppn]["AuteurCats"]
            if sorter != "":
                parentcats += '[[' + commonsAuteurCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsAuteurCat + ']]\n'

        if "UitgeverCats" in catsdata[ppn]:
            commonsUitgeverCat = catsdata[ppn]["UitgeverCats"]
            if sorter != "":
                parentcats += '[[' + commonsUitgeverCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsUitgeverCat + ']]\n'

        if "DescriptionCats" in catsdata[ppn]:
            commonsDescriptionCat = catsdata[ppn]["DescriptionCats"]
            if sorter != "":
                parentcats += '[[' + commonsDescriptionCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsDescriptionCat + ']]\n'

        if "AlternativeCats" in catsdata[ppn]:
            commonsAlternativeCat = catsdata[ppn]["AlternativeCats"]
            if sorter != "":
                parentcats += '[[' + commonsAlternativeCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsAlternativeCat + ']]\n'

        #Write Glamorous page stats ==
        glamorous = "Usage statistics"

        # ======================================================
        # Create Book template in every Homecat # See e.g. https://commons.wikimedia.org/wiki/Category:De_Nieuwe_Rijschool

        BookTemplate = "BOOKTEMPLATE"


    #================================================================
    # Write final strings to API

        # 1-- Title van de Homecat
        title = str(commonsHomeCat) #eg. Category:Moeder Hubbard en haar hond
        # 2--Wat er in de bewerkingsaamenvatting zou komen
        summary = 'Creating ' + commonsHomeCat
        # 3-- Tekstuele inhoud van de Homecat
        message += BookTemplate + glamorous + parentcats

        #print('PDCounter: ' + str(pd_counter))
        #print('PPN: '+ ppn)
        print('Homecat: ' + title)
        print('Summary: ' + summary)
        print("Message: " + message)
        print("=======================================")

        #Schrijf naar de Commons-API
        payload = {'action': 'edit', 'assert': 'user', 'format': 'json', 'utf8': '', 'appendtext': message,'summary': summary, 'title': title, 'token': edit_token}
        r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)
        print (r4.text)

print("Number of PD books: "+str(pd_counter))
data_file.close()
catsfile.close()
npagesfile.close()
gwtbasetitlefile.close()