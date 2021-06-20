from urllib.parse import unquote
from pathlib import Path
import os
from passivlingo_dictionary.helpers.Constants import OWN_TO_NLTK_LANGMAP
from passivlingo_dictionary.helpers.Constants import OWN_TO_NLTK_LANGMAP_EXCLUSIONS
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP_EXCLUSIONS
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS_OWN

class CommonHelper:

    @classmethod
    def getLangVariant(cls, filterLang):
        result = [filterLang]
        
        langMap = {}
        langMap.update(OWN_TO_NLTK_LANGMAP)
        langMap.update(OWN_TO_NLTK_LANGMAP_EXCLUSIONS)
        try:
            variant = CommonHelper.getWordnetLanguageCode(filterLang, VALID_WORDNET_LANGS, langMap)
            result.append(variant)
            return result
        except:
            pass 

        langMap = {}
        langMap.update(NLTK_TO_OWN_LANGMAP)
        langMap.update(NLTK_TO_OWN_LANGMAP_EXCLUSIONS)
        try:
            variant = CommonHelper.getWordnetLanguageCode(filterLang, VALID_WORDNET_LANGS_OWN, langMap)   
            result.append(variant)
            return result
        except:
            pass    

        return result

    @classmethod
    def getWordnetLanguageCode(cls, lang, validLangs, langMap):
        if lang == None:
            return None

        if lang in validLangs:
            return lang

        result = langMap.get(lang)
        if result != None:
            return result        

        raise ValueError(f"Invalid Language Code: '{lang}' is not a valid wordnet language code")                 

    @classmethod
    def getCountryCode(cls, lang):
        choices = {'fra': 'fr', 'spa': 'es', 'ita': 'it', 'nld': 'nl', 'por' : 'pt', 'ger': 'de', 'eng': 'en', 'fas': 'fa', 'jpn': 'ja', 'pol': 'pl', 'tha': 'th'}
        return choices.get(lang, 'en')

    @classmethod
    def getNewsApiCountryCode(cls, lang):
        choices = {'fra': 'fr', 'spa': 'mx', 'ita': 'it', 'nld': 'nl', 'por' : 'pt', 'ger': 'de', 'eng': 'gb'}
        return choices.get(lang, 'gb')        

    @classmethod
    def getWordnetLangDescription(cls, lang):
        choices = {'fra': 'french', 'spa': 'spanish', 'ita': 'italian', 'nld': 'dutch', 'por' : 'portuguese', 'ger': 'german', 'eng': 'english'}
        return choices.get(lang, 'english')

    @classmethod
    def getSpacyModelName(cls, lang):
        modelName = CommonHelper.__getSpacyModelName(lang)        
        if os.path.isdir(os.path.join(Path.home(), '.spacy_data')):
            return os.path.join(Path.home(), '.spacy_data', modelName)
        else:
            return modelName    

    @classmethod
    def __getSpacyModelName(cls, lang):
        if lang in ['fra', 'fr']:
            return 'fr_core_news_sm'
        if lang in ['spa', 'es']:
            return 'es_core_news_sm'            
        if lang in ['ita', 'it']:
            return 'it_core_news_sm'            
        if lang in ['nld', 'nl']:
            return 'nl_core_news_sm'                        
        if lang in ['por', 'pt']:
            return 'pt_core_news_sm'                        
        if lang in ['ger', 'de', 'deu']:
            return 'de_core_news_sm'   
        if lang in ['cmn', 'zh']:                                 
            return 'zh_core_web_sm'
        if lang in ['dan', 'da']:                                 
            return 'da_core_news_sm'            
        if lang in ['ell', 'el']:                                 
            return 'el_core_news_sm'
        if lang in ['jpn', 'jp']:                                 
            return 'ja_core_news_sm'
        if lang in ['lit', 'lt']:                                 
            return 'lt_core_news_sm'                                                
        if lang in ['nno', 'nob', 'nb']:                                 
            return 'nb_core_news_sm'            
        if lang in ['pol', 'pl']:                                 
            return 'pl_core_web_sm'
        if lang in ['ron', 'ro']:                                 
            return 'ro_core_news_sm'                                                        

        return 'en_core_web_sm'        

    @classmethod
    def getSpacyToWordnetPosMapping(cls, pos):
        choices = {'VERB': 'v', 'NOUN': 'n', 'ADV': 'r', 'ADJ': 'a'}
        return choices.get(pos, 'x')

    @classmethod
    def getWordnetPosMapping(cls, pos):
        if pos.startswith('NN'):
            return 'n'
        elif pos.startswith('VB'):
            return 'v'
        elif pos.startswith('JJ'):
            return 'a'
        elif pos.startswith('RB'):
            return 'r'
        else:
            return 'x'

    @classmethod
    def sanatizeWord(cls, woi):        
        result = unquote(woi)
        startsWithList = ["...", "'",'"', "n'", "l'", ",", ".", "!", "?", "¿", ";", "_", "-", "`", "~", "<", ">", "%", "$", "#", "*", "(", ")", "+", "|", "@", "&", "^", "«", "»"]
        endsWithList = ["...", "'",'"', "'s", ",", ".", "!", "?", "¿",";", "_", "-", "`", "~", "<", ">", "%", "$", "#", "*", "(", ")", "+", "|", "@", "&", "^", "«", "»"]
        for s in startsWithList:
            if result.startswith(s):
                result = result[len(s):]
        for e in endsWithList:
            if result.endswith(e):
                result = result[:(len(e)*-1)]                

        return result        
    
