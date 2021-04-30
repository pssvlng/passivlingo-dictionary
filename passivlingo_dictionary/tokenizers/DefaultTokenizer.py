from .Tokenizer import Tokenizer
import nltk
from nltk.corpus import stopwords
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from passivlingo_dictionary.helpers.Constants import DOMAIN_NAMES
from passivlingo_dictionary.models.ContextWord import ContextWord

class DefaultTokenizer(Tokenizer):

    def __init__(self, words, lang):
        super().__init__(words, lang)

    def tokenize(self):     
        result = []           
        self.tokens = nltk.word_tokenize(self.words)        
        stopWords = set(stopwords.words(CommonHelper.getWordnetLangDescription(self.lang)))
        self.tokens = [t for t in self.tokens if not t.lower() in stopWords] 
        self.tokens = [t for t in self.tokens if not any(s in t.lower() for s in DOMAIN_NAMES)] 
        self.tokens = [t for t in self.tokens if len(t) > 1]

        #remove words with apostrofe
        self.tokens = [t for t in self.tokens if "'" not in t]
        #remove end of sentence elipse
        self.tokens = [t for t in self.tokens if "..." not in t]
        #remove double quotes
        self.tokens = [t for t in self.tokens if "`" not in t]        
        self.tokens = [t for t in self.tokens if '"' not in t]        

        for t in self.tokens:
            word = ContextWord()
            word.name = t
            word.pos = 'x'
            word.lemma = t
            result.append(word)        
        return result
    
