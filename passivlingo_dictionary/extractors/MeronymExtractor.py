from .Extractor import Extractor

class MeronymExtractor(Extractor):

    def __init__(self, wordNetWrapper):
        super().__init__(wordNetWrapper)
        
    def extract(self, pSynsets):
        return self.wordNetWrapper.getMeronyms(pSynsets)

    def __repr__(self):
        return f'MeronymExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'MeronymExtractor({repr(self.wordNetWrapper)})'                                 