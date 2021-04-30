from .WordSenseProvider import WordSenseProvider
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

class EnglishWordSenseProvider(WordSenseProvider):    
    
    def getWordIdentifier(self, word, pos, sentence):              
        tokens = word_tokenize(sentence)
        result = lesk(tokens, word, pos=pos)        
        if result is not None:
            return [(result.name()), (result.offset())]

        return [(''), ('')]