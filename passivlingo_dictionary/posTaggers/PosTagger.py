from abc import abstractmethod, ABCMeta

class PosTagger:

    __metaclass__ = ABCMeta
   
    @abstractmethod
    def tagText(self, textToTag): pass