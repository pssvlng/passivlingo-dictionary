import spacy
from .PosTagger import PosTagger
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper

class SpacyPosTagger(PosTagger):    
    def __init__(self, lang):        
        self.nlp = spacy.load(CommonHelper.getSpacyModelName(lang))

    def tagText(self, textToTag):                  
        words = self.nlp(textToTag)                        
        result = []
        for word in words:            
            result.append((word.text, word.pos_, word.lemma_))
        return result


