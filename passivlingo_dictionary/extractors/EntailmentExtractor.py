from .Extractor import Extractor

class EntailmentExtractor(Extractor):

    def __init__(self, wordNetWrapper):
        super().__init__(wordNetWrapper)

    def extract(self, pSynsets):        
        return self.wordNetWrapper.getEntailments(pSynsets)

    def __repr__(self):
        return f'EntailmentExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'EntailmentExtractor({repr(self.wordNetWrapper)})'      