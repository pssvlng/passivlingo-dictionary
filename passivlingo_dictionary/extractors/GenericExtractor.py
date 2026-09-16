from .Extractor import Extractor

class GenericExtractor(Extractor):

    def __init__(self, pExtractList, wordNetWrapper):        
        super().__init__(wordNetWrapper)
        self.extractList = pExtractList

    def extract(self, pSynsets):
        result = []
        for r in self.extractList:
            result.extend(r.extract(pSynsets))
        return result

    def __repr__(self):
        return f'GenericExtractor({repr(self.wordNetWrapper)})'