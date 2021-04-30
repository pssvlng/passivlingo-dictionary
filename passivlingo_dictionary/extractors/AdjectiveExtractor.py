from .Extractor import Extractor

class AdjectiveExtractor(Extractor):
    
    def __init__(self, wordNetWrapper):
        super().__init__(wordNetWrapper)

    def extract(self, pSynsets):
        result = []
        result = self.wordNetWrapper.getWordByPos(pSynsets, 'a', self.wordNetWrapper.getPOSDescription('a'))
        result.extend(self.wordNetWrapper.getWordByPos(pSynsets, 's', self.wordNetWrapper.getPOSDescription('s')))
        return result

    def __repr__(self):
        return f'AdjectiveExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'AdjectiveExtractor({repr(self.wordNetWrapper)})'    