class OwnSynsetWrapper:

    def __init__(self, lang, synset):
        self.__lang = lang
        self.__synset = synset
    
    @property
    def id(self):
        return self.__synset.id
    @property
    def ili(self):
        try:
            if self.__synset.ili:            
                return self.__synset.ili.id
        except:
            return ''
            
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
        result = self.__synset.examples()                    
        for sense in self.__synset.senses():
            result.extend(sense.examples())
        return result
    def hypernyms(self):
        result = []
        for synset in self.__synset.hypernyms():
            result.append(OwnSynsetWrapper(self.lang, synset))
        return result
    def hyponyms(self):
        result = []
        for synset in self.__synset.hyponyms():
            result.append(OwnSynsetWrapper(self.lang, synset))
        return result    
    def meronyms(self):
        result = []
        for synset in self.__synset.meronyms():
            result.append(OwnSynsetWrapper(self.lang, synset))
        return result        
    def holonyms(self):
        result = []
        for synset in self.__synset.holonyms():
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
