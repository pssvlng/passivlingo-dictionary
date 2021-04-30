from .PosTagger import PosTagger
import nltk

class NltkPosTagger(PosTagger):    
        
    def tagText(self, textToTag):                  
        tokens = nltk.word_tokenize(textToTag)                
        return nltk.pos_tag(tokens)        
    
