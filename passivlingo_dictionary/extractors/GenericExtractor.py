from .Extractor import Extractor

class GenericExtractor(Extractor):

    def __init__(self, pExtractList, wordNetWrapper):        
        super().__init__(wordNetWrapper)
        self.extractList = pExtractList

    def extract(self, pSynsets):
        for r in self.extractList:
            r.extract(pSynsets)

    def __repr__(self):
        return f'GenericExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'GenericExtractor({repr(self.wordNetWrapper)})'              