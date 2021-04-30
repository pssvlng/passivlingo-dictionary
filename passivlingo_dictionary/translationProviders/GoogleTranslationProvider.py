from .TranslationProvider import TranslationProvider
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from urllib.request import Request, urlopen
import urllib.parse
import json

class GoogleTranslationProvider(TranslationProvider):
    def __init__(self, googleApiKey):        
        self.baseUrl = 'https://translation.googleapis.com/language/translate/v2?format=text&key=' + googleApiKey +'&q='
    
    def translate(self, sourceLang, targetLang, woi):                       
        url = self.baseUrl + urllib.parse.quote(woi) + '&target=' + targetLang                
        try:
            req = Request(url)
            req.add_header('User-Agent', '')            
            response = urlopen(req)            
            if (str(response.status) != '200'):
                print("Google Api could not translate '%s' into target language '%s'" % (woi, targetLang))
                return ''        

            result = []
            jsonresponse = json.loads(response.read().decode('utf-8'))        
            for tr in jsonresponse['data']['translations']:                
                result.append(tr['translatedText'])
            
            return ', '.join(result)
        except Exception as err:            
            print("Google Api could not translate '%s' into target language '%s': %s" % (woi, targetLang, err))
            return ''    
