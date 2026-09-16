from .TranslationProvider import TranslationProvider

class EmptyTranslationProvider(TranslationProvider):
    def __init__(self):        
        self.baseUrl = ''
    
    def translate(self, sourceLang, targetLang, woi):         
        return ''    
