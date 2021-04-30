from abc import abstractmethod, ABCMeta

class Extractor:

    __metaclass__ = ABCMeta

    def __init__(self, wordNetWrapper):        
        self.wordNetWrapper = wordNetWrapper

    @abstractmethod
    def extract(self, pSynsets): pass  
    
 