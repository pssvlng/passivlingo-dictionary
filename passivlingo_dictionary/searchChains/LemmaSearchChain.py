from .SearchChain import SearchChain
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods
from passivlingo_dictionary.extractors.CombinedExtractor import CombinedExtractor
from textblob import TextBlob

class LemmaSearchChain(SearchChain):

    def __init__(self, woi, lang, wordNetWrapper):
        super().__init__(woi, lang)
        self.wordNetWrapper = wordNetWrapper
    
    def execute(self):        
        result = []
        if self.lang == None:
            blob = TextBlob(self.woi)                        
            try:
                self.lang = self.wordNetWrapper.getWordnetLanguageCode(blob.detect_language())
            except:
                return super().execute()
        
        lemmaList = FactoryMethods.getLemmatizer(self.lang).lemmatize(self.woi)        
        for w in lemmaList:
           localSynsets = self.wordNetWrapper.translate(w, self.lang)
           result = result + CombinedExtractor(self.wordNetWrapper).extract(localSynsets)

        if len(result) > 0:
            return result   

        return super().execute()

    def __repr__(self):
        return f'LemmaSearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'LemmaSearchChain({self.woi} {repr(self.wordNetWrapper)})'