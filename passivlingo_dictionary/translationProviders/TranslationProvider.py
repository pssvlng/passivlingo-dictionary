from abc import abstractmethod, ABCMeta

class TranslationProvider:

    __metaclass__ = ABCMeta    

    @abstractmethod
    def translate(self, sourceLang, targetLang, woi): pass