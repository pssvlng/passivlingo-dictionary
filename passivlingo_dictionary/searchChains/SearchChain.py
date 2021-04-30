from abc import abstractmethod, ABCMeta

class SearchChain:

    __metaclass__ = ABCMeta

    def __init__(self, woi, lang, continueIfResults = False):        
        self.woi = woi
        self.lang = lang        
        self.continueIfResults= continueIfResults
        
    @abstractmethod
    def execute(self):        
        return []
    