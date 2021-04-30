from .TranslationProvider import TranslationProvider
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from urllib.request import Request, urlopen
import urllib.parse
import json

class EmptyTranslationProvider(TranslationProvider):
    def __init__(self):        
        self.baseUrl = ''
    
    def translate(self, sourceLang, targetLang, woi):         
        return ''    
