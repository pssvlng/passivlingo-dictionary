from abc import abstractmethod, ABCMeta

class WordNetWrapper:

    __metaclass__ = ABCMeta    

    @abstractmethod    
    def getPOSDescription(self, pos): pass                

    @abstractmethod        
    def getWordByPos(self, pSynsets, classifier, posDescription): pass

    @abstractmethod                
    def getWord(self, synset): pass
        
    @abstractmethod            
    def getLinguisticCounter(self, pSynset): pass        
    
    @abstractmethod        
    def getSynonyms(self, pSynset, pName): pass        

    @abstractmethod        
    def getAntonyms(self, pSynsets): pass        
    
    @abstractmethod        
    def getHolonyms(self, pSynsets): pass        

    @abstractmethod        
    def getHypernyms(self, pSynsets): pass        

    @abstractmethod        
    def getHyponyms(self, pSynsets): pass        

    @abstractmethod        
    def getMeronyms(self, pSynsets): pass        

    @abstractmethod        
    def getEntailments(self, pSynsets): pass        
    
    #TODO: Deprecated - remove method
    @abstractmethod        
    def getLanguageDescriptions(self, pSynset): pass

    @abstractmethod        
    def getGenericLanguageDescriptions(self, pSynset): pass
        
    @abstractmethod                    
    def getLanguageStr(self, pSynset, plang): pass
    
    @abstractmethod                    
    def translatePos(self, woi, posToken, lang): pass        

    @abstractmethod                    
    def translate(self, woi, lang = None): pass

    @abstractmethod                    
    def getWordKey(self, wordkey): pass

    @abstractmethod                    
    def isValidWordKey(self, wordkey): pass

    @abstractmethod                    
    def getWordKeySynset(self, wordkey, lang): pass

    @abstractmethod                    
    def filterResults(self, result, items): pass

    @abstractmethod
    def getWordnetLanguageCode(self, lang): pass        

    @abstractmethod
    def getWordsFromIli(self, ili, lang): pass        

    @abstractmethod
    def getSynsetsFromIli(self, ili, lang): pass        
        
    