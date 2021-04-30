from .Extractor import Extractor

class HolonymExtractor(Extractor):

    def __init__(self, wordNetWrapper):
        super().__init__(wordNetWrapper)

    def extract(self, pSynsets):
        return self.wordNetWrapper.getHolonyms(pSynsets)     

    def __repr__(self):
        return f'HolonymExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'HolonymExtractor({repr(self.wordNetWrapper)})'                     