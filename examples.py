from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam
from passivlingo_dictionary.TextProcessor import TextProcessor

#========================
# Word Search Examples  
#========================

def basicWordSearch():
    myDict = Dictionary()
    
    #Setup the search parameter to pass into the dictionary
    searchParam = SearchParam()
    #Specify the word to search for: woi = Word of Interest
    searchParam.woi = 'house'    
    #If searchParam.filterLang property is left empty,
    #then the search will find results in the most important EU languages: EN, DE, FR, ES, IT, PT, NL
    
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

    #to filter on more than one language, use a comma to separate language pairs
    searchParam.filterLang = 'de, fr, en, pt, arb, cat'
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

def iliLookup():
    myDict = Dictionary()        
    searchParam = SearchParam()    
    searchParam.woi = 'happy'
    searchParam.wordnetId = 'own'
    result = myDict.findWords(searchParam)
    #print example sentences
    print(myDict.getExampleSentences(result[0].wordKey))

    #find correpsonding Italian words and example sentences
    searchParam.reset()
    searchParam.ili = result[0].ili
    searchParam.lang = 'it'
    result2 = myDict.findWords(searchParam)
    print(result2)
    print(myDict.getExampleSentences(result2[0].wordKey))

basicWordSearch()
basicWordSearchWithLanguageFilter()
categorySearchHypernym()
categorySearchEntailment()
categorySearchAntonym()
nltkOnlySearch()
ownOnlySearch()
iliLookup()

#===============================
# Basic Text Processing Examples  
#===============================

def simpleTextProcessing():
    sentence = 'The big black dogs came into the living room quietly.'
    txtProcessor = TextProcessor()
    
    #This will extract words with the following pos tags: Noun, Verb, Adverb, Adjective
    result = txtProcessor.tokenizeSentence(sentence, 'en')
    # = dogs
    print(result[2].name)
    # = dog
    print(result[2].lemma)
    # = Noun
    print(result[2].pos)

    myDict = Dictionary()
    searchParam = SearchParam()
    #woi and lemma required
    searchParam.woi = result[2].name
    searchParam.lemma = result[2].lemma
    searchParam.pos = result[2].pos    
    searchParam.lang = 'en'

    #returns all words that has value of 'dog' and has pos of 'Noun' in Wordnet
    result2 = myDict.findWords(searchParam)
    print(result2)

simpleTextProcessing()