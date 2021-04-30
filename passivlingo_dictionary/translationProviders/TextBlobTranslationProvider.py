from .TranslationProvider import TranslationProvider
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from textblob import TextBlob

class TextBlobTranslationProvider(TranslationProvider):
    
    def translate(self, sourceLang, targetLang, woi):                 
        blob = TextBlob(woi)
        try:
            result = str(blob.translate(to=targetLang))
            return result
        except:
            return ''    
