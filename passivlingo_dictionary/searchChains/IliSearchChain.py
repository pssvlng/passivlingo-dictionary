from .SearchChain import SearchChain
from passivlingo_dictionary.extractors.CombinedExtractor import CombinedExtractor
from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper
import wn

class IliSearchChain(SearchChain):

    def __init__(self, ili, lang, wordNetWrapper):
        super().__init__('', lang)
        self.ili = ili
        self.wordNetWrapper = wordNetWrapper
    
    def execute(self):                
        lang = self.wordNetWrapper.getWordnetLanguageCode(self.lang)

        result = []        
        for synset in wn.synsets(ili=self.ili, lang=lang):
            result.append(self.wordNetWrapper.getWord(OwnSynsetWrapper(lang, synset)))

        return result            

    def __repr__(self):
        return f'IliSearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'IliSearchChain({self.woi} {repr(self.wordNetWrapper)})'