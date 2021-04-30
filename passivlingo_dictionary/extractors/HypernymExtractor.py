from .Extractor import Extractor

class HypernymExtractor(Extractor):
    
    def __init__(self, wordNetWrapper):
        super().__init__(wordNetWrapper)

    def extract(self, pSynsets):
        return self.wordNetWrapper.getHypernyms(pSynsets)

    def __repr__(self):
        return f'HypernymExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'HypernymExtractor({repr(self.wordNetWrapper)})'                         