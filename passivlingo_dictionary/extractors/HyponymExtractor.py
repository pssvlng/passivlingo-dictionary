from .Extractor import Extractor

class HyponymExtractor(Extractor):

    def __init__(self, wordNetWrapper):
        super().__init__(wordNetWrapper)
        
    def extract(self, pSynsets):
        return self.wordNetWrapper.getHyponyms(pSynsets)

    def __repr__(self):
        return f'HyponymExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'HyponymExtractor({repr(self.wordNetWrapper)})'                             