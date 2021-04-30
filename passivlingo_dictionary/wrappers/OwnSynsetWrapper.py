class OwnSynsetWrapper:

    def __init__(self, lang, synset):
        self.__lang = lang
        self.__synset = synset
    
    @property
    def id(self):
        return self.__synset.id
    @property
    def ili(self):
        if self.__synset.ili:
            return self.__synset.ili.id
        return ''
    @property
    def pos(self):
        return self.__synset.pos
    @property
    def lang(self):
        return self.__lang

    def senses(self):
        return self.__synset.senses()            
    def lemmas(self):
        return self.__synset.lemmas()            
    def definition(self):
        return self.__synset.definition()            
    def examples(self):
        return self.__synset.examples()                    
    def hypernyms(self):
        result = []
        for synset in self.__synset.hypernyms():
            result.append(OwnSynsetWrapper(self.lang, synset))
        return result
    def get_related(self, relation):
        result = []
        for synset in self.__synset.get_related(relation):
            result.append(OwnSynsetWrapper(self.lang, synset))
        return result        

    def __repr__(self):
        return f'OwnSynsetWrapper({self.id})'
    def __str__(self):        
        return f'OwnSynsetWrapper({self.id})'
