from abc import abstractmethod, ABCMeta
from urllib.parse import unquote
from passivlingo_dictionary.wordSenseProviders.DefaultWordSenseProvider import DefaultWordSenseProvider
from passivlingo_dictionary.wordSenseProviders.EnglishWordSenseProvider import EnglishWordSenseProvider

class Tokenizer:

    __metaclass__ = ABCMeta

    def __init__(self, words, lang):        
        self.words = words
        self.lang = lang                

    def tokenizeSentence(self, words): 
        if words == None:
            words = ''
        self.words = unquote(words)
        return self.tokenize()        
    
    @classmethod
    def getWordSenseProvider(cls, lang):
        choices = {'eng': EnglishWordSenseProvider()}
        return choices.get(lang, DefaultWordSenseProvider())

    @abstractmethod
    def tokenize(self): pass
    