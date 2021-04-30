from .Tokenizer import Tokenizer
from passivlingo_dictionary.helpers.Constants import DOMAIN_NAMES
from nltk.corpus import stopwords
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from passivlingo_dictionary.models.ContextWord import ContextWord

class GenericTokenizer(Tokenizer):

    def __init__(self, words, lang, posTagger, useDisambiguation = False):
        super().__init__(words, lang)        
        self.posTagger = posTagger
        self.useDisambiguation = useDisambiguation
        self.wordSenseProvider = Tokenizer.getWordSenseProvider(self.lang)        

    def tokenize(self):     
        result = []                           
        wordTags = self.posTagger.tagText(self.words)        
        stopWords = set(stopwords.words(CommonHelper.getWordnetLangDescription(self.lang)))
        wordTags = [t for t in wordTags if not t[0].lower() in stopWords] 
        wordTags = [t for t in wordTags if not any(s in t[0].lower() for s in DOMAIN_NAMES)]         
        wordTags = [t for t in wordTags if t[1] in ['VERB', 'NOUN', 'ADV', 'ADJ']]        

        #remove words with apostrofe
        wordTags = [t for t in wordTags if "'" not in t[0]]
        #remove end of sentence elipse                    
        wordTags = [t for t in wordTags if "..." not in t[0]]
        wordTags = [t for t in wordTags if "…" not in t[0]]
        #remove double quotes
        wordTags = [t for t in wordTags if "`" not in t[0]]
        wordTags = [t for t in wordTags if '"' not in t[0]]
        
        for t in wordTags:            
            word = ContextWord()
            word.name = t[0]
            word.pos = CommonHelper.getSpacyToWordnetPosMapping(t[1])     
            if self.useDisambiguation:
                wordIdentifier = self.wordSenseProvider.getWordIdentifier(word.name, word.pos, self.words)
                word.wordKey = wordIdentifier[0]
                word.offset = wordIdentifier[1]         
            word.lemma = t[2]
            result.append(word)        
        return result
