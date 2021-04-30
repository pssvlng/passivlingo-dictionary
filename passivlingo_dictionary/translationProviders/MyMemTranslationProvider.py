from .TranslationProvider import TranslationProvider
from urllib.parse import quote
from urllib.request import Request, urlopen
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
import json

class MyMemTranslationProvider(TranslationProvider):
    
    def translate(self, sourceLang, targetLang, woi):         
        
        url = 'https://api.mymemory.translated.net/get?q=' + quote(woi) + '&langpair=' + sourceLang + '|' + targetLang            
        req = Request(url)
        req.add_header('User-Agent', '')
        response = urlopen(req)
        if (str(response.status) == '200'):
            jsonresponse = json.loads(response.read().decode('utf-8'))
            if (str(jsonresponse['responseStatus']) == '200'):                                        
                return jsonresponse['responseData']['translatedText']
                    
        return ''                