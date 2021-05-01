from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam

def basicWordSearch():
    myDict = Dictionary()
    
    #Setup the search parameter to pass into the dictionary
    searchParam = SearchParam()
    #Specify the word to search for: woi = Word of Interest
    searchParam.woi = 'happy'
    #If searchParam.filterLang property is left empty,
    #then the search will use most important EU languages: EN, DE, FR, ES, IT, PT, NL
    
    result = myDict.findWords(searchParam)
    print(result)

def basicWordSearchWithLanguageFilter():
    myDict = Dictionary()        
    searchParam = SearchParam()    
    searchParam.woi = 'Häuser'
    #set language filter to German (de)    
    searchParam.filterLang = 'de'
    result = myDict.findWords(searchParam)
    print(result)    

def categorySearchHypernym():
    #Step1: search for the initial word
    myDict = Dictionary()        
    searchParam = SearchParam()    
    searchParam.woi = 'vehicle'
    result = myDict.findWords(searchParam)

    #Step2: search for the derivates of word found in step 1 based on a specified category
    #Available categories: antonym, hypernym, hyponym, holonym, meronym, entailment
    #The language of the word found in step 1 also needs to be included
    searchParam.reset()
    searchParam.wordkey = result[0].wordKey
    searchParam.category = 'hypernym'
    searchParam.lang = result[0].lang
    result2 = myDict.findWords(searchParam)
    print(result2)

def categorySearchEntailment():
    #Step1: search for the initial word
    myDict = Dictionary()        
    searchParam = SearchParam()    
    searchParam.woi = 'snore'
    result = myDict.findWords(searchParam)

    #Step2: set category as entailment
    verbs = [x for x in result if x.pos == 'Verb']
    searchParam.reset()
    searchParam.wordkey = verbs[0].wordKey
    searchParam.category = 'entailment'
    searchParam.lang = verbs[0].lang
    result2 = myDict.findWords(searchParam)

    #Should contain the verb 'to sleep'
    print(result2)

def categorySearchAntonym():
    myDict = Dictionary()        
    searchParam = SearchParam()    
    searchParam.woi = 'happy'
    result = myDict.findWords(searchParam)

    searchParam.reset()
    searchParam.wordkey = result[0].wordKey
    searchParam.category = 'antonym'
    searchParam.lang = result[0].lang
    result2 = myDict.findWords(searchParam)

    #result2 should contain 'unhappy'    
    print(result2)

def nltkOnlySearch():    
    myDict = Dictionary()        
    searchParam = SearchParam()    
    searchParam.woi = 'happy'
    searchParam.wordnetId = 'nltk'
    result = myDict.findWords(searchParam)

    #only results from nltk wordnet
    print(result)

def ownOnlySearch():    
    myDict = Dictionary()        
    searchParam = SearchParam()    
    searchParam.woi = 'happy'
    searchParam.wordnetId = 'own'
    result = myDict.findWords(searchParam)

    #only results from own wordnet
    print(result)

basicWordSearch()
basicWordSearchWithLanguageFilter()
categorySearchHypernym()
categorySearchEntailment()
categorySearchAntonym()
nltkOnlySearch()
ownOnlySearch()
