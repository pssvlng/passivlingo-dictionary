from .SearchChain import SearchChain
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods

class CategorySearchChain(SearchChain):

    def __init__(self, category, woi, lang, wordNetWrapper):
        super().__init__(woi, lang)
        self.category = category
        self.wordNetWrapper = wordNetWrapper

    def execute(self):        
        extractor = FactoryMethods.getExtractor(self.category, self.wordNetWrapper)

        if extractor != None:            
            synsets = self.wordNetWrapper.translate(self.woi, self.lang)
            return extractor.extract(synsets)

        return super().execute()

    def __repr__(self):
        return f'CategorySearchChain({self.category} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'CategorySearchChain({self.category} {repr(self.wordNetWrapper)})'                                         
