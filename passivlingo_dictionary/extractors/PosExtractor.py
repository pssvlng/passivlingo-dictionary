from .Extractor import Extractor

class PosExtractor(Extractor):

    def __init__(self, wordNetWrapper, pos):    
        self.pos = pos
        super().__init__(wordNetWrapper)

    def extract(self, pSynsets):
        return self.wordNetWrapper.getWordByPos(pSynsets, self.pos, self.wordNetWrapper.getPOSDescription(self.pos))

    def __repr__(self):
        return f'PosExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'PosExtractor({repr(self.wordNetWrapper)})'                                     