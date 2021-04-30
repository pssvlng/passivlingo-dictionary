from .WordSenseProvider import WordSenseProvider

class DefaultWordSenseProvider(WordSenseProvider):    
    
    def getWordIdentifier(self, word, pos, sentence):              
        return [(''), ('')]