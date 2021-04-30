from abc import abstractmethod, ABCMeta

class WordSenseProvider:

    __metaclass__ = ABCMeta
   
    @abstractmethod
    def getWordIdentifier(self, word, pos, sentence): pass