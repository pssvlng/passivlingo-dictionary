from .SearchChain import SearchChain
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods

class PosSearchChain(SearchChain):

    def __init__(self, pos, woi, lang, wordNetWrapper):
        super().__init__(woi, lang)
        self.pos = pos
        self.wordNetWrapper = wordNetWrapper

    def execute(self):        
        extractor = FactoryMethods.getExtractorByPos(self.pos, self.wordNetWrapper)

        if extractor != None:            
            if self.pos not in ['n', 'v', 'r', 'a']:
                synsets = self.wordNetWrapper.translate(self.woi, self.lang)
            else:
                synsets = self.wordNetWrapper.translatePos(self.woi, self.pos, self.lang)
            
            result = extractor.extract(synsets)
            if len(result) > 0:
                return result

        return super().execute()

    def __repr__(self):
        return f'PosSearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'PosSearchChain({self.woi} {repr(self.wordNetWrapper)})'    
