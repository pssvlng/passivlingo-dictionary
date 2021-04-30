from passivlingo_dictionary.models.SearchParam import SearchParam
from passivlingo_dictionary.helpers.SearchChainFactory import SearchChainFactory
from passivlingo_dictionary.helpers.Constants import WORDNET_IDENTIFIER_OWN
from passivlingo_dictionary.helpers.Constants import WORDNET_IDENTIFIER_NLTK
from nltk.corpus import wordnet as nltk_wn
import wn

class Dictionary:

    def findWords(self, searchParam: SearchParam):
        if searchParam.wordnetId not in [WORDNET_IDENTIFIER_OWN, WORDNET_IDENTIFIER_NLTK]:
            searchParam.wordnetId = WORDNET_IDENTIFIER_OWN    
        
        results = []
        for item in SearchChainFactory().getSearchChains(searchParam):
            results.extend(item.execute())

        return results

    def getExampleSentences(self, wordKey: str, wordnetId= WORDNET_IDENTIFIER_OWN):
        if len(wordKey.split('.')) < 3:
            raise ValueError('Invalid word key')

        if wordnetId not in [WORDNET_IDENTIFIER_NLTK, WORDNET_IDENTIFIER_OWN]:
            wordnetId = WORDNET_IDENTIFIER_OWN
        
        wnToUse = wn if wordnetId == WORDNET_IDENTIFIER_OWN else nltk_wn
        synset = wnToUse.synset(wordKey)

        return synset.examples()
    
    def __repr__(self):
        return 'Dictionary()'
    def __str__(self):    
        return 'Dictionary()'
        

