# Python Standard Library
import requests
import os
import re   # regex
import requests

# Import Python 3rd Party Libraries
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import nltk     # Import the Natural Language Toolkit
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag

# Pseudo Constants
AUTHOR = "Joshua Wren"
CREATION_DATE = "11 May 2021"
TITLE = "Week Sixteen - Final Project - Web Scraper, FIND ALL THE THINGS!"
IMG_SAVE = "./SCRAPED_IMAGES/"  # Directory to store images

# Create the directory if necessary
if not os.path.exists(IMG_SAVE):
    os.makedirs(IMG_SAVE)

print(AUTHOR)
print(CREATION_DATE)
print(TITLE, "\n")

def main():
    table = PrettyTable()
    table.title = 'Webpage Information'
    table.field_names = ['Link','Title', 'Page Links', 'Image Links', 'Unique Vocabulary', 'Proper Names', 'Nouns', 'Verbs', 'Adjectives']    
    
    print("Example Website:\nhttps://casl.website")
    target = input("Please input a website: ")
    
    def soupifyPage(webpage):
        page = requests.get(webpage)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
        
    mainSoup = soupifyPage(target)
    
    def getPageTitle(webpage):
        '''Gets title from page'''
        s = soupifyPage(webpage)
        print("\nExtracting Title from: ", webpage)
        print("Please Wait\n")
        
        pageTitle = s.find('title').string
        print(f"Page Title: {pageTitle}")
        return pageTitle
    
    mainTitle = getPageTitle(target)
    
    def getPageLinks(webpage):
        '''Gets all links from page'''
        s = soupifyPage(webpage)
        print("\nExtracting Links from: ", target)
        print("Please Wait\n")
        
        pageLinks = s.findAll('a', href=True)  # Find the link (a) tags with reference (href)
        linkURLSet = set()
        
        for link in pageLinks:      # Process and display each link
            try:
                linkURL = link['href']
                print("Processing Link:", linkURL, end="")
                if linkURL[0:4] != 'http':       # If URL path is relative
                    linkURL = target+linkURL         # try prepending the base url
        
                response = requests.get(linkURL)                 # Get the link from the URL
                linkName = os.path.basename(linkURL)
                
                print(f"  >> Link: {linkURL}")
            except Exception as err:
                print(linkURL, err)
                continue
            linkURLSet.add(linkURL)
            
        return linkURLSet
    
    mainLinks = getPageLinks(target)
    
    def concatenateForColumn(iterable):
        separator = '\n'
        iterableAsOneString = separator.join(iterable)     # join by separator
        return iterableAsOneString
    
    mainLinksString = concatenateForColumn(mainLinks)
        
    def getPageImgs(webpage):
        '''Gets all images from page'''
        s = soupifyPage(webpage)
        print("\nExtracting Images from: ", target)
        print("Please Wait\n")
        
        pageImages = s.findAll('img')  # Find the image tags
        imgURLSet = set()
        
        for image in pageImages:      # Process and display each image
            try:
                imgURL = image['src']
                print("Processing Image:", imgURL, end="")
                if imgURL[0:4] != 'http':       # If URL path is relative
                    imgURL = target+imgURL         # try prepending the base url
        
                response = requests.get(imgURL)                 # Get the image from the URL
                imageName = os.path.basename(imgURL)            
                
                imgOutputPath = IMG_SAVE+imageName
                
                with open(imgOutputPath, 'wb') as outFile:
                    outFile.write(response.content)
                    
                # Save the image
                print(f"  >> Saved Image: {imgOutputPath}")
            except Exception as err:
                print(imgURL, err)
                continue
            imgURLSet.add(imgURL)
        
        return imgURLSet
    
    mainURLs = getPageImgs(target)
    mainimgURLString = concatenateForColumn(mainURLs)
    
    def getUniqueWords(webpage):
        soupy = soupifyPage(webpage)
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(soupy.get_text())
        filteredTokens = [w for w in tokens if not w in stop_words]
        filteredTokens = []
        for w in tokens:
            if w not in stop_words:
                filteredTokens.append(w)    
        '''Get unique words'''
        print("\nExtracting Unique Words from: ", webpage)
        print("Please Wait\n")
            
        pageWords = set()
        for word in filteredTokens:
            pageWords.add(str(word))
        sortedPageWords = sorted(pageWords)
        return sortedPageWords
    
    def getUniquePropers(webpage):
        uniques = getUniqueWords(webpage)
        funcList = []
        for word,pos in nltk.pos_tag(uniques):
            if (pos == 'NNP'):
                funcList.append(word)
            elif (pos == 'NNPS'):
                funcList.append(word)
        print('Extraction of Unique Propers completed\n')
        return funcList
    
    def getUniqueNouns(webpage):
        uniques = getUniqueWords(webpage)
        funcList = []
        for word,pos in nltk.pos_tag(uniques):
            if (pos == 'NN'):
                funcList.append(word)
            elif (pos == 'NNS'):
                funcList.append(word)
        print('Extraction of Unique Nouns completed\n')
        return funcList        
    
    def getUniqueVerbs(webpage):
        uniques = getUniqueWords(webpage)
        funcList = []
        for word,pos in nltk.pos_tag(uniques):
            if (pos == 'VB'):
                funcList.append(word)
            elif (pos == 'VBD'):
                funcList.append(word)
            elif (pos == 'VBG'):
                funcList.append(word)
            elif (pos == 'VBN'):
                funcList.append(word)
            elif (pos == 'VBP'):
                funcList.append(word)
            elif (pos == 'VBZ'):
                funcList.append(word)
        print('Extraction of Unique Verbs completed\n')
        return funcList                  
    
    def getUniqueAdjectives(webpage):
        uniques = getUniqueWords(webpage)
        funcList = []
        for word,pos in nltk.pos_tag(uniques):
            if (pos == 'JJ'):
                funcList.append(word)
            elif (pos == 'JJR'):
                funcList.append(word)
            elif (pos == 'JJS'):
                funcList.append(word)
        print('Extraction of Unique Adjectives completed\n')
        return funcList
    
    mainSortedPageWords = getUniqueWords(target)
    print('Extraction of Unique Words completed\n')
    mainPropersList     = getUniquePropers(target)
    mainNounsList       = getUniqueNouns(target)
    mainVerbsList       = getUniqueVerbs(target)
    mainAdjectivesList  = getUniqueAdjectives(target)
    
    mainWordsListString      = concatenateForColumn(mainSortedPageWords)
    mainPropersListString    = concatenateForColumn(mainPropersList)
    mainNounsListString      = concatenateForColumn(mainNounsList)
    mainVerbsListString      = concatenateForColumn(mainVerbsList)
    mainAdjectivesListString = concatenateForColumn(mainAdjectivesList)
    
    
    table.add_row([str(target), str(mainTitle), str(mainLinksString), str(mainimgURLString), str(mainWordsListString), str(mainPropersListString), str(mainNounsListString), str(mainVerbsListString), str(mainAdjectivesListString)])
    print('Table row added...')
    table.align = 'l'
    
    '''repeat most of above for sublinks to mainpage'''
    for link in mainLinks:
        subSoup = soupifyPage(link)
        subTitle = getPageTitle(link)
        subLinks = getPageLinks(link)
        subLinksString = concatenateForColumn(subLinks)
        subURLs = getPageImgs(link)
        subimgURLString = concatenateForColumn(subURLs)
        subSortedPageWords = getUniqueWords(link)
        print('Extraction of Unique Words completed\n')
        subPropersList     = getUniquePropers(link)
        subNounsList       = getUniqueNouns(link)
        subVerbsList       = getUniqueVerbs(link)
        subAdjectivesList  = getUniqueAdjectives(link)
        
        subWordsListString      = concatenateForColumn(subSortedPageWords)
        subPropersListString    = concatenateForColumn(subPropersList)
        subNounsListString      = concatenateForColumn(subNounsList)
        subVerbsListString      = concatenateForColumn(subVerbsList)
        subAdjectivesListString = concatenateForColumn(subAdjectivesList)
        
        
        table.add_row([str(link), str(subTitle), str(subLinksString), str(subimgURLString), str(subWordsListString), str(subPropersListString), str(subNounsListString), str(subVerbsListString), str(subAdjectivesListString)])
        print('Table row added...')
    
    '''print prettytable'''
    print('Table created\n\nOutputting results...\n')
    print(table)
    
    '''Output table to txt file'''
    print('\nTable being put into txt file...\n')
    table_txt = table.get_string()
    with open('wrenJ_WK16-1_PrettyTableOutput.txt','w') as file:
        file.write(table_txt)
    print('Txt file creation complete\n')
        
if __name__ == '__main__':
    main()    
    print("\nScrape Script Complete")