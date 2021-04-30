from .SearchChain import SearchChain
from passivlingo_dictionary.extractors.CombinedExtractor import CombinedExtractor

class DefaultSearchChain(SearchChain):

    def __init__(self, woi, lang, wordNetWrapper):
        super().__init__(woi, lang)
        self.wordNetWrapper = wordNetWrapper
    
    def execute(self):        
        synsets = self.wordNetWrapper.translate(self.woi, self.lang)                    
        if len(synsets) > 0:
            return CombinedExtractor(self.wordNetWrapper).extract(synsets)    

        return super().execute()

    def __repr__(self):
        return f'DefaultSearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'DefaultSearchChain({self.woi} {repr(self.wordNetWrapper)})'                                             
        
