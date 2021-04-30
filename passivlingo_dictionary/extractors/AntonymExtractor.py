from .Extractor import Extractor

class AntonymExtractor(Extractor):

    def __init__(self, wordNetWrapper):
        super().__init__(wordNetWrapper)

    def extract(self, pSynsets):
        return self.wordNetWrapper.getAntonyms(pSynsets)

    def __repr__(self):
        return f'AntonymExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'AntonymExtractor({repr(self.wordNetWrapper)})'        