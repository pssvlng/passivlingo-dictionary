from .SearchChain import SearchChain
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods

class WordKeySearchChain(SearchChain):

    def __init__(self, category, woi, lang, wordNetWrapper):
        super().__init__(woi, lang)
        self.category = category
        self.wordNetWrapper = wordNetWrapper

    def execute(self):                
        extractor = FactoryMethods.getExtractor(self.category, self.wordNetWrapper)
        if extractor != None:
            if self.wordNetWrapper.isValidWordKey(self.woi):
                synset = self.wordNetWrapper.getWordKeySynset(self.wordNetWrapper.getWordKey(self.woi), self.lang)
                return extractor.extract([synset])            

        return super().execute()

    def __repr__(self):
        return f'WordKeySearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'WordKeySearchChain({self.woi} {repr(self.wordNetWrapper)})'    
