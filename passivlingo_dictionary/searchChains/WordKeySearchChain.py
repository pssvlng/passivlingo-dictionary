from .SearchChain import SearchChain
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods

class WordKeySearchChain(SearchChain):

    def __init__(self, category, woi, lang, wordNetWrapper):
        super().__init__(woi, lang)
        self.category = category
        self.wordNetWrapper = wordNetWrapper

    def execute(self):                
        extractor = FactoryMethods.getExtractor(self.category, self.wordNetWrapper)
        synset = None
        if extractor != None:
            result = []
            if self.wordNetWrapper.isValidWordKey(self.woi):
                synset = self.wordNetWrapper.getWordKeySynset(self.wordNetWrapper.getWordKey(self.woi), self.lang)
                result = extractor.extract([synset])
                if len(result) > 0:
                    return result

            en_synsets = []
            if self.lang not in ['en', 'eng']:
                lang = self.wordNetWrapper.getWordnetLanguageCode('en')
                if synset:
                    if synset.ili: 
                        en_synsets.extend(self.wordNetWrapper.getSynsetsFromIli(synset.ili, lang))

                return extractor.extract(en_synsets)             

        return super().execute()

    def __repr__(self):
        return f'WordKeySearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'WordKeySearchChain({self.woi} {repr(self.wordNetWrapper)})'    
