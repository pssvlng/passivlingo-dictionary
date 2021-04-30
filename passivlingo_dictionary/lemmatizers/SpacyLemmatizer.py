from .Lemmatizer import Lemmatizer
import spacy
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper

class SpacyLemmatizer(Lemmatizer):

    def __init__(self, lang):
        self.nlp = spacy.load(CommonHelper.getSpacyModelName(lang))

    def lemmatize(self, woi):     
        words = []        
        if len(woi.split(' ')) > 1:                   
            words.append(' '.join([i.text for i in self.nlp(woi.title())]))
            words.append(' '.join([i.text for i in self.nlp(woi.lower())]))        
        else:
          words = self.nlp(' '.join([woi.title(), woi.lower()]))
          words = map(lambda x: x.lemma_, words)

        result = list(words)
        if woi in result:
            result.remove(woi)
        return list(set(result))