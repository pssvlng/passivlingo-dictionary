from nltk.corpus import wordnet as wn
from passivlingo_dictionary.models.Word import Word
import copy
from passivlingo_dictionary.models.LinguisticCounter import LinguisticCounter
from passivlingo_dictionary.models.LanguageDescriptions import LanguageDescriptions
from passivlingo_dictionary.models.GenericLanguageDescriptions import GenericLanguageDescriptions
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS
from passivlingo_dictionary.helpers.Constants import VALID_EU_LANGS
from passivlingo_dictionary.helpers.Constants import OWN_TO_NLTK_LANGMAP
from passivlingo_dictionary.helpers.Constants import OWN_TO_NLTK_LANGMAP_EXCLUSIONS
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from .WordNetWrapper import WordNetWrapper
from passivlingo_dictionary.searchChains.CategorySearchChain import CategorySearchChain
from passivlingo_dictionary.searchChains.WordKeySearchChain import WordKeySearchChain

class NltkWordNetWrapper(WordNetWrapper):
    
    def __init__(self, filterLang):
        if filterLang:
            self.filterLang = ['eng']
            for lang in filterLang.split(','):
                self.filterLang.append(self.getWordnetLanguageCode(lang))
            self.filterLang = list(set(self.filterLang))
        else:
            self.filterLang = ['fra', 'ita', 'spa', 'por', 'nld']    
            
    def getPOSDescription(self, pos):   
        if pos in ['t', 'c', 'p']:
            return 'Unknown'

        if pos == wn.VERB:
            return 'Verb'
        if pos == wn.NOUN:
            return 'Noun'
        if pos == wn.ADJ:
            return 'Adjective'
        if pos == wn.ADV:
            return 'Adverb'
        if pos == wn.ADJ_SAT:
            return 'Adjective'                

        raise ValueError(f'Unknown POS: {pos}. Unable to find corresponding description')         
    
    def getWordByPos(self, pSynsets, classifier, posDescription):         
        result = []
        for synset in pSynsets:
            if synset.name().split('.')[1] == classifier:
                item = Word()
                item.lang = 'en'
                item.wordnetId = 'nltk'
                item.name = synset.name().split('.')[0].replace('_', ' ')
                item.pos = posDescription                
                item.definition = synset.definition()                
                item.example = synset.examples()[0] if len(synset.examples()) > 0 else ''
                item.offset = synset.offset()
                item.wordKey = synset.name()
                item.LinguisticCounter = self.getLinguisticCounter(synset)
                #TODO: Deprecated - use only GenericLanguageDescriptions object in future
                item.LanguageDescriptions = self.getLanguageDescriptions(synset)
                item.GenericLanguageDescriptions = self.getGenericLanguageDescriptions(synset)
                item.synonyms = self.getSynonyms(synset, synset.name().split('.')[0])
                result.append(item)

        return result        
        
    def getWord(self, synset): 
        result = Word()
        result.lang = 'en'
        result.wordnetId = 'nltk'
        result.name = synset.name().split('.')[0].replace('_', ' ')
        result.pos = self.getPOSDescription(synset.name().split('.')[1])       
        result.definition = synset.definition()                
        result.example = synset.examples()[0] if len(synset.examples()) > 0 else ''
        result.offset = synset.offset()
        result.wordKey = synset.name()
        result.LinguisticCounter = self.getLinguisticCounter(synset)
        #TODO: Deprecated - use only GenericLanguageDescriptions object in future
        result.LanguageDescriptions = self.getLanguageDescriptions(synset)
        result.GenericLanguageDescriptions = self.getGenericLanguageDescriptions(synset)
        result.synonyms = self.getSynonyms(synset, synset.name().split('.')[0])
        
        return result        
    
    def getLinguisticCounter(self, pSynset): 
        result = LinguisticCounter()
        count = 0
        for lemma in pSynset.lemmas():
            count = count + len(lemma.antonyms())
        result.antonym = count
        result.hypernym = len(pSynset.hypernyms())
        result.hyponym = len(pSynset.hyponyms())
        result.holonym = len(pSynset.member_holonyms()) + len(pSynset.part_holonyms())
        result.meronym = len(pSynset.member_meronyms()) + len(pSynset.part_meronyms())
        result.entailment = len(pSynset.entailments())
        result.mt = 1

        return result    
    
    def getSynonyms(self, pSynset, pName):
        results = pSynset.lemma_names()        
        if pName in results:
            results.remove(pName)    
        results = [w.replace('_', ' ') for w in results]

        return results    

    def getAntonyms(self, pSynsets):
        results = []        
        for synset in pSynsets:
            for lemma in synset.lemmas():
                for a in lemma.antonyms():
                    results.append(self.getWord(a.synset()))
                    
        return results      

    def getEntailments(self, pSynsets):
        results = []
        for synset in pSynsets:
            for synset2 in synset.entailments():
                results.append(self.getWord(synset2))
        return results               

    def getHolonyms(self, pSynsets):
        results = []
        #MEMBER HOLONYMS
        for synset in pSynsets:
            for synset2 in synset.member_holonyms():
                results.append(self.getWord(synset2))
        #PART HOLONYMS
        for synset in pSynsets:
            for synset2 in synset.part_holonyms():
                results.append(self.getWord(synset2))
        return results

    def getHypernyms(self, pSynsets):
        results = []
        for synset in pSynsets:
            for synset2 in synset.hypernyms():
                results.append(self.getWord(synset2))
        return results    

    def getHyponyms(self, pSynsets): 
        results = []
        for synset in pSynsets:
            for synset2 in synset.hyponyms():
                results.append(self.getWord(synset2))
        return results

    def getMeronyms(self, pSynsets): 
        results = []
        #MEMBER MERONYMS
        for synset in pSynsets:
            for synset2 in synset.member_meronyms():
                results.append(self.getWord(synset2))
        #PART MERONYMS
        for synset in pSynsets:
            for synset2 in synset.part_meronyms():
                results.append(self.getWord(synset2))
        return results        
    
    def getLanguageDescriptions(self, pSynset):
        result = LanguageDescriptions()                

        for lang in self.filterLang:
            result.setWordDescription(lang, self.getLanguageStr(pSynset, lang).replace("_", " "))        
        
        return result
    
    def getGenericLanguageDescriptions(self, pSynset):
        result = GenericLanguageDescriptions()                        

        for lang in self.filterLang:
            result.setWordDescription(lang, self.getLanguageStr(pSynset, lang).replace("_", " "))        
        
        return result

    def getLanguageStr(self, pSynset, plang):    
        result = ''
        filterlist = ['GAP!', 'PSEUDOGAP!']
        for lemma in pSynset.lemmas(lang=plang):
            if lemma.name() not in filterlist:
                result = result + lemma.name() + ', '
        if len(result) > 0:
            result = result[:-2]    

        return result

    def translatePos(self, woi, posToken, lang):
        woi = woi.replace(" ", "_")
        
        if lang not in VALID_WORDNET_LANGS:
            return []
        woi = wn.synsets(woi, lang=lang, pos=posToken)
        return woi

    def translate(self, woi, lang = None):
        woi = woi.replace(" ", "_")

        result = []        
        if lang == None:
            for l in self.filterLang:
                result = result + wn.synsets(woi, lang=l)

        if len(result) > 0:
            return result

        if lang not in VALID_WORDNET_LANGS:
            return []
    
        return wn.synsets(woi, lang=lang)

    def isValidWordKey(self, wordkey):
        wordkeyArr = wordkey.split('.')
        return len(wordkeyArr) == 3

    def getWordKey(self, wordkey):         
        return wordkey

    def getWordKeySynset(self, wordkey, lang):
        return wn.synset(wordkey)       

    def filterResults(self, result, items):
        #if self.filterLang is not None and not any(isinstance(val, (CategorySearchChain, WordKeySearchChain)) for val in items):    
        #    return list(filter(lambda x: x.LanguageDescriptions.getWordDescription(self.filterLang) != '', result))            
        return result                   
    
    def getWordnetLanguageCode(self, lang):
        langMap = {}
        langMap.update(OWN_TO_NLTK_LANGMAP)
        langMap.update(OWN_TO_NLTK_LANGMAP_EXCLUSIONS)
        return CommonHelper.getWordnetLanguageCode(lang, VALID_WORDNET_LANGS, langMap)

    def __repr__(self):
        return 'NltkWordNetWrapper()'
    def __str__(self):    
        return 'NltkWordNetWrapper()'
