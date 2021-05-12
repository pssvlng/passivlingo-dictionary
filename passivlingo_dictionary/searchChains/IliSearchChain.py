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
        return self.wordNetWrapper.getWordsFromIli(self.ili, self.lang)                

    def __repr__(self):
        return f'IliSearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'IliSearchChain({self.woi} {repr(self.wordNetWrapper)})'