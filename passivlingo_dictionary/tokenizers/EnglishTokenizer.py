from .Tokenizer import Tokenizer
import nltk
from passivlingo_dictionary.helpers.Constants import DOMAIN_NAMES
from nltk.corpus import stopwords
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from passivlingo_dictionary.models.ContextWord import ContextWord

class EnglishTokenizer(Tokenizer):

    def __init__(self, words, lang):
        super().__init__(words, lang)

    def tokenize(self):     
        result = []           
        self.tokens = nltk.word_tokenize(self.words)                
        wordTags = nltk.pos_tag(self.tokens)
        wordTags = [w for w in wordTags if w[1] not in ["NNP", "NNPS", "CD", "EX", "FW", "IN"]]                
        stopWords = set(stopwords.words(CommonHelper.getWordnetLangDescription(self.lang)))
        wordTags = [t for t in wordTags if not t[0].lower() in stopWords] 
        wordTags = [t for t in wordTags if not any(s in t[0].lower() for s in DOMAIN_NAMES)] 
        wordTags = [t for t in wordTags if len(t[0]) > 1]

        #remove words with apostrofe
        wordTags = [t for t in wordTags if "'" not in t[0]]
        #remove end of sentence elipse
        wordTags = [t for t in wordTags if "..." not in t[0]]
        #remove double quotes
        wordTags = [t for t in wordTags if "`" not in t[0]]
        wordTags = [t for t in wordTags if '"' not in t[0]]

        for t in wordTags:
            word = ContextWord()
            word.name = t[0]
            word.pos = CommonHelper.getWordnetPosMapping(t[1])
            word.lemma = t[0]
            result.append(word)        
        return result
    
