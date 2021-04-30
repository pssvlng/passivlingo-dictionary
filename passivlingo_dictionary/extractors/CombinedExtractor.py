from .Extractor import Extractor
from .AdjectiveExtractor import AdjectiveExtractor
from .PosExtractor import PosExtractor

class CombinedExtractor(Extractor):

    def __init__(self, wordNetWrapper):
        super().__init__(wordNetWrapper)

    def extract(self, pSynsets):
        result = []
        result = PosExtractor(self.wordNetWrapper, 'n').extract(pSynsets)
        result.extend(PosExtractor(self.wordNetWrapper, 'v').extract(pSynsets))
        result.extend(AdjectiveExtractor(self.wordNetWrapper).extract(pSynsets))
        result.extend(PosExtractor(self.wordNetWrapper, 'r').extract(pSynsets))
        result.extend(PosExtractor(self.wordNetWrapper, 't').extract(pSynsets))
        result.extend(PosExtractor(self.wordNetWrapper, 'c').extract(pSynsets))
        result.extend(PosExtractor(self.wordNetWrapper, 'p').extract(pSynsets))
        return result    

    def __repr__(self):
        return f'CombinedExtractor({repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'CombinedExtractor({repr(self.wordNetWrapper)})'         