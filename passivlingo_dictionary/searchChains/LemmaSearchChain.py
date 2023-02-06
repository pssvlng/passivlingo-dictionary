from .SearchChain import SearchChain
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods
from passivlingo_dictionary.extractors.CombinedExtractor import CombinedExtractor
from textblob import TextBlob

class LemmaSearchChain(SearchChain):

    def __init__(self, woi, lang, wordNetWrapper, filterLang=''):
        super().__init__(woi, lang)
        self.wordNetWrapper = wordNetWrapper
        self.filterLang = filterLang
    
    def execute(self):        
        result = []
        def combineResults(lemmaList, lang):
            for w in lemmaList:
                localSynsets = self.wordNetWrapper.translate(w, lang)
                result.extend(CombinedExtractor(self.wordNetWrapper).extract(localSynsets))

        try:
            if self.lang == None:
                for lang in self.filterLang.split(','):        
                    combineResults(FactoryMethods.getLemmatizer(lang).lemmatize(self.woi), lang)                        
            else:
                combineResults(FactoryMethods.getLemmatizer(self.lang).lemmatize(self.woi), self.lang)                                                                
        
        except:
            pass

        if len(result) > 0:
            return result   

        return super().execute()

    def __repr__(self):
        return f'LemmaSearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'LemmaSearchChain({self.woi} {repr(self.wordNetWrapper)})'