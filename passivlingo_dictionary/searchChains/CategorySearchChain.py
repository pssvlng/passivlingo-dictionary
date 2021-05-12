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
            result = extractor.extract(synsets)
            if len(result) > 0:
                return result

            en_synsets = []
            if self.lang not in ['en', 'eng']:
                lang = self.wordNetWrapper.getWordnetLanguageCode('en')
                for synset in synsets:
                    if synset.ili:
                        en_synsets.append(self.wordNetWrapper.getWordsFromIli(synset.ili, lang))

                return extractor.extract(en_synsets)                            

        return super().execute()

    def __repr__(self):
        return f'CategorySearchChain({self.category} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'CategorySearchChain({self.category} {repr(self.wordNetWrapper)})'                                         
