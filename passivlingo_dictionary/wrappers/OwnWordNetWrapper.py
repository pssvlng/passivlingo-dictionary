import wn
import copy
from functools import reduce
from passivlingo_dictionary.models.Word import Word
from passivlingo_dictionary.models.LinguisticCounter import LinguisticCounter
from passivlingo_dictionary.models.LanguageDescriptions import LanguageDescriptions
from passivlingo_dictionary.models.GenericLanguageDescriptions import GenericLanguageDescriptions
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS_OWN
from passivlingo_dictionary.helpers.Constants import VALID_EU_LANGS_OWN
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP_EXCLUSIONS
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from .WordNetWrapper import WordNetWrapper
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods
from .OwnSynsetWrapper import OwnSynsetWrapper

class OwnWordNetWrapper(WordNetWrapper):
    
    def __init__(self, filterLang):
        if filterLang:
            self.filterLang = ['en']
            for lang in filterLang.split(','):
                self.filterLang.append(self.getWordnetLanguageCode(lang))
            self.filterLang = list(set(self.filterLang))    
        else:
            self.filterLang = copy.deepcopy(VALID_EU_LANGS_OWN)    
            
    def getPOSDescription(self, pos):   
        if pos == wn.constants.VERB:
            return 'Verb'
        if pos == wn.constants.NOUN:
            return 'Noun'
        if pos == wn.constants.ADJ:
            return 'Adjective'
        if pos == wn.constants.ADV:
            return 'Adverb'
        if pos == wn.constants.ADJ_SAT:
            return 'Adjective'  
        if pos == wn.constants.PHRASE:
            return 'Phrase'           
        if pos == wn.constants.CONJUNCTION:
            return 'Conjunction'                       
        if pos == wn.constants.ADPOSITION:
            return 'Adposition'                           
        if pos == wn.constants.OTHER:
            return 'Other'
        if pos == wn.constants.UNKNOWN:
            return 'Unknown'                                           

        raise ValueError(f'Unknown POS: {pos}. Unable to find corresponding description')         
    
    def getWordByPos(self, pSynsets, classifier, posDescription): 
        result = []
        for synset in pSynsets:            
            if synset.pos == classifier:
                item = Word()
                item.name = synset.lemmas()[0].replace('_', ' ')
                item.pos = posDescription                
                item.definition = synset.definition()                
                item.example = synset.examples()[0] if len(synset.examples()) > 0 else ''
                item.offset = synset.id.split('-')[1]
                item.ili = synset.ili
                item.wordKey = '.'.join([synset.lemmas()[0], synset.pos, synset.id.split('-')[1], synset.id.split('-')[0]])
                item.linguisticCounter = self.getLinguisticCounter(synset)
                #TODO: Deprecated - use only GenericLanguageDescriptions object in future
                item.languageDescriptions = self.getLanguageDescriptions(synset)
                item.genericLanguageDescriptions = self.getGenericLanguageDescriptions(synset)
                item.synonyms = self.getSynonyms(synset, synset.lemmas()[0])
                item.lang = synset.lang                
                item.wordnetId = 'own'
                result.append(item)

        return result        
        
    def getWord(self, synset): 
        result = Word()
        result.name = synset.lemmas()[0].replace('_', ' ')
        result.pos = self.getPOSDescription(synset.id.split('-')[2])       
        result.definition = synset.definition()                
        result.example = synset.examples()[0] if len(synset.examples()) > 0 else ''
        result.offset = synset.id.split('-')[1]
        result.ili = synset.ili
        result.wordKey = '.'.join([synset.lemmas()[0], synset.pos, synset.id.split('-')[1], synset.id.split('-')[0]])
        result.linguisticCounter = self.getLinguisticCounter(synset)
        #TODO: Deprecated - use only GenericLanguageDescriptions object in future
        result.languageDescriptions = self.getLanguageDescriptions(synset)
        result.genericLanguageDescriptions = self.getGenericLanguageDescriptions(synset)
        result.synonyms = self.getSynonyms(synset, synset.lemmas()[0])
        result.lang = synset.lang
        result.wordnetId = 'own'

        return result        
    
    def getLinguisticCounter(self, pSynset): 
        result = LinguisticCounter()
        count = 0        
        for sense in pSynset.senses():
            count = count + len(sense.get_related('antonym'))        
        result.antonym = count
        result.hypernym = len(pSynset.hypernyms())
        result.hyponym = len(pSynset.get_related('hyponym'))
        result.holonym = len(pSynset.get_related('holo_member')) + len(pSynset.get_related('holo_part'))
        result.meronym = len(pSynset.get_related('mero_member')) + len(pSynset.get_related('mero_part'))
        result.entailment = len(pSynset.get_related('entails'))        
        result.mt = 1

        return result    
    
    def getSynonyms(self, pSynset, pName):
        results = pSynset.lemmas()        
        if pName in results:
            results.remove(pName)    
        results = [w.replace('_', ' ') for w in results]

        return results    

    def getAntonyms(self, pSynsets):
        result = []
        for synset in pSynsets:
            for sense in synset.senses():
                for relatedSense in sense.get_related('antonym'):
                    wrapperToAdd = OwnSynsetWrapper(synset.lang, relatedSense.synset())
                    if len(list(filter(lambda x: x.ili == wrapperToAdd.ili, result))) == 0:                        
                        result.append(self.getWord(wrapperToAdd))                            
        
        return result

    def getEntailments(self, pSynsets):
        results = []
        for synset in pSynsets:
            for synset2 in synset.get_related('entails'):
                results.extend(self.__getRelationalSynsets(synset2))
        return results 

    def getHolonyms(self, pSynsets):
        results = []
        #MEMBER HOLONYMS
        for synset in pSynsets:
            for synset2 in synset.get_related('holo_member'):
                results.extend(self.__getRelationalSynsets(synset2))
        #PART HOLONYMS
        for synset in pSynsets:
            for synset2 in synset.get_related('holo_part'):
                results.extend(self.__getRelationalSynsets(synset2))
        return results

    def getHypernyms(self, pSynsets):
        results = []
        for synset in pSynsets:
            for synset2 in synset.hypernyms():
                results.extend(self.__getRelationalSynsets(synset2))
        return results    

    def getHyponyms(self, pSynsets): 
        results = []
        for synset in pSynsets:
            for synset2 in synset.get_related('hyponym'):                
                results.extend(self.__getRelationalSynsets(synset2))
        return results

    def getMeronyms(self, pSynsets):     
        results = []
        #MEMBER MERONYMS
        for synset in pSynsets:
            for synset2 in synset.get_related('mero_member'):
                results.extend(self.__getRelationalSynsets(synset2))
        #PART MERONYMS
        for synset in pSynsets:
            for synset2 in synset.get_related('mero_part'):
                results.extend(self.__getRelationalSynsets(synset2))
        return results       

    def __getRelationalSynsets(self, synset):
        results = []
        if synset.id == '*INFERRED*':                  
            for inferredSynset in wn.synsets(ili=synset.ili, lang='en'):
                wrapperToAdd = OwnSynsetWrapper('en', inferredSynset)
                if len(list(filter(lambda x: x.ili == wrapperToAdd.ili, results))) == 0:                        
                    results.append(self.getWord(wrapperToAdd))    
        else:            
            results.append(self.getWord(synset))

        return results

    def getLanguageDescriptions(self, pSynset):
        result = LanguageDescriptions()                        
        langList = copy.deepcopy(self.filterLang)
        
        if (pSynset.lang in langList):
            langList.remove(pSynset.lang)     
                
        if (pSynset.ili):        
            for lang in langList:
                result.setWordDescription(lang, self.getLanguageStr(pSynset, lang).replace("_", " "))        
        
        return result

    def getGenericLanguageDescriptions(self, pSynset):
        result = GenericLanguageDescriptions()                        
        langList = copy.deepcopy(self.filterLang)
        
        if (pSynset.lang in langList):
            langList.remove(pSynset.lang)     
                
        if (pSynset.ili):        
            for lang in langList:
                result.setWordDescription(lang, self.getLanguageStr(pSynset, lang).replace("_", " "))        
        
        return result
    
    def getLanguageStr(self, pSynset, plang):      
        plang = self.getWordnetLanguageCode(plang)              
        result = []
        for synset in wn.synsets(ili=pSynset.ili, lang=plang):
            result = result + synset.lemmas()

        return ','.join(result)
        
    def translatePos(self, woi, posToken, lang):
        lang = self.getWordnetLanguageCode(lang)
        
        if lang not in VALID_WORDNET_LANGS_OWN:
            return []

        return FactoryMethods.getOwnSynsetWrappers(wn.synsets(woi, lang=lang, pos=posToken), lang)        

    def translate(self, woi, lang = None):   
        lang = self.getWordnetLanguageCode(lang)         
        result = []
        if lang == None:            
            for l in self.filterLang:
                result = result + FactoryMethods.getOwnSynsetWrappers(wn.synsets(woi, lang=l), l)
        
        if len(result) > 0:
            return result

        if lang not in VALID_WORDNET_LANGS_OWN:
            return []

        return FactoryMethods.getOwnSynsetWrappers(wn.synsets(woi, lang=lang), lang)

    def isValidWordKey(self, wordkey):
        wordkeyArr = wordkey.split('.')
        return len(wordkeyArr) == 4

    def getWordKey(self, wordkey): 
        wordkeyArr = wordkey.split('.')
        return '-'.join([wordkeyArr[3], wordkeyArr[2], wordkeyArr[1]])

    def getWordKeySynset(self, wordkey, lang):
        lang = self.getWordnetLanguageCode(lang)
        return OwnSynsetWrapper(lang, wn.synset(wordkey))        

    def filterResults(self, result, items):
        return result

    def getWordnetLanguageCode(self, lang):
        langMap = {}
        langMap.update(NLTK_TO_OWN_LANGMAP)
        langMap.update(NLTK_TO_OWN_LANGMAP_EXCLUSIONS)
        return CommonHelper.getWordnetLanguageCode(lang, VALID_WORDNET_LANGS_OWN, langMap)
    
    def __repr__(self):
        return 'OwnWordNetWrapper()'
    def __str__(self):    
        return 'OwnWordNetWrapper()'
        
    
