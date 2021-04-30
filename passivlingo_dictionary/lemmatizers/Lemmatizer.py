from abc import abstractmethod, ABCMeta

class Lemmatizer:

    __metaclass__ = ABCMeta

    @abstractmethod
    def lemmatize(self, woi): pass  