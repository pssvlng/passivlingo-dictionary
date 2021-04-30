from .SearchChain import SearchChain

class ContainerSearchChain(SearchChain):

    def __init__(self, items, woi, lang, wordNetWrapper):
        super().__init__(woi, lang)
        self.items = items
        self.wordNetWrapper = wordNetWrapper

    def execute(self):       
        result = [] 
        for item in self.items:
            result = result + self.wordNetWrapper.filterResults(item.execute(), self.items)
            if len(result) > 0 and not item.continueIfResults:
                return result        

        if len(result) > 0:
            return result            

        return super().execute()    

    def __repr__(self):
        return f'ContainerSearchChain({self.woi} {repr(self.wordNetWrapper)})'
    def __str__(self):    
        return f'ContainerSearchChain({self.woi} {repr(self.wordNetWrapper)})'                                         

        
        