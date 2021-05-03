from .BaseWord import BaseWord

class Word(BaseWord):           
    def __init__(self):
        super().__init__()                
        self.definition = ''
        self.example = ''        
        self.linguisticCounter = None
        self.languageDescriptions = None
        self.genericLanguageDescriptions = None
        self.synonyms = ''

    def __repr__(self):
        return f'Word({self.wordKey})'

    def __str__(self):        
        return f'Word({self.wordKey})'    