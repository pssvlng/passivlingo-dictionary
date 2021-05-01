from .SearchChain import SearchChain
from passivlingo_dictionary.helpers.Constants import VALID_EU_LANGS_OWN
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS_OWN
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP_EXCLUSIONS
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from passivlingo_dictionary.models.Word import Word
from passivlingo_dictionary.models.LanguageDescriptions import LanguageDescriptions
from passivlingo_dictionary.models.GenericLanguageDescriptions import GenericLanguageDescriptions
from passivlingo_dictionary.models.LinguisticCounter import LinguisticCounter

class MTSearchChain(SearchChain):

    def __init__(self, translationProvider, woi, lang, filterLang):
        super().__init__(woi, lang)
        self.translationProvider = translationProvider        
        self.filterLang = filterLang
    
    def execute(self):             
        result = Word()       
        result.name = self.woi.replace("_", " ")                            
        result.pos = 'Machine Translation'
        result.LinguisticCounter = LinguisticCounter()
        result.LanguageDescriptions = LanguageDescriptions()  
        result.GenericLanguageDescriptions = GenericLanguageDescriptions()      
        
        langList = ['en'] + self.filterLang.split(',') if self.filterLang else VALID_EU_LANGS_OWN
        langMap = {}
        langMap.update(NLTK_TO_OWN_LANGMAP)
        langMap.update(NLTK_TO_OWN_LANGMAP_EXCLUSIONS)
        for item in langList:
            try:
                item = CommonHelper.getWordnetLanguageCode(item, VALID_WORDNET_LANGS_OWN, langMap)
            except:
                pass    
        langList = list(set(langList))    

        for lang in langList:
            translation = self.translationProvider.translate(None, lang, result.name)
            result.LanguageDescriptions.setWordDescription(lang, translation)
            result.GenericLanguageDescriptions.setWordDescription(lang, translation)        

        if result.name.strip() == '':            
            return super().execute()

        if result.LanguageDescriptions.getWordDescriptions('') == '':
            return super().execute()

        return [result]

    def __repr__(self):
        return f'MTSearchChain({self.woi})'
    def __str__(self):    
        return f'MTSearchChain({self.woi})'