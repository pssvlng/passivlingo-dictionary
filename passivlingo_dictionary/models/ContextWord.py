from .BaseWord import BaseWord

class ContextWord(BaseWord):           
    def __init__(self):
        super().__init__()                
        self.lemma = ''

    def __str__(self):
        return f'ContextWord({self.lemma})'

    def __repr__(self):
        return f'ContextWord({self.lemma})'
    