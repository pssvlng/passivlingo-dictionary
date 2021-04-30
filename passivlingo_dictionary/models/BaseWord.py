from abc import abstractmethod, ABCMeta

class BaseWord:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = ''
        self.pos = ''
        self.offset = ''
        self.wordKey = ''
        self.ili = ''
        self.lang = ''
        self.wordnetId = ''
        
    def __str__(self):
        return f'BaseWord({self.wordKey})'

    def __repr__(self):
        return f'BaseWord({self.wordKey})'
        
