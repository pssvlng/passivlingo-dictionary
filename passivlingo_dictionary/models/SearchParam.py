class SearchParam:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.wordkey = None
        self.category = None
        self.lang = None
        self.woi = None
        self.lemma = None
        self.pos = None
        self.filterLang = None
        self.wordnetId = None
        self.googleApiKey = None
        self.ili = None

    def __repr__(self):
        return f'SearchParam({self.woi} {self.wordKey} {self.filterLang})'
    def __str__(self):    
        return f'SearchParam({self.woi} {self.wordKey} {self.filterLang})'