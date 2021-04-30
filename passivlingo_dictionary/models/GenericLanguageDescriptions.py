from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS_OWN
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP_EXCLUSIONS

class GenericLanguageDescriptions:
    def __init__(self):
        self.descriptionLookup = {}
        self.langMap = {}
        self.langMap.update(NLTK_TO_OWN_LANGMAP)
        self.langMap.update(NLTK_TO_OWN_LANGMAP_EXCLUSIONS)

        for key in list(self.langMap.keys()):
            self.descriptionLookup.update({self.langMap[key]: ''})

    def getWordDescription(self, lang):        
        if lang in list(self.descriptionLookup.keys()):
            return self.descriptionLookup.get(lang)

        result = self.langMap.get(lang)
        if result != None:
            return self.descriptionLookup.get(result)        

        raise ValueError(f"Invalid Language Code: '{lang}' is not a valid wordnet language code")                            

    def setWordDescription(self, lang, woi):                
        if lang in list(self.descriptionLookup.keys()):
            self.descriptionLookup[lang] = woi
            return

        result = self.langMap.get(lang)
        if result != None:
            self.descriptionLookup[result] = woi        
            return

        raise ValueError(f"Invalid Language Code: '{lang}' is not a valid wordnet language code")

    def __repr__(self):
        return f'GenericLanguageDescriptions({len(self.langMap)})'

    def __str__(self):        
        return f'GenericLanguageDescriptions({len(self.langMap)})'    