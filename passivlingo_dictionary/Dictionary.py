""" Passivlingo Multilingual Dictionary 
Copyright (C) Passivlingo (www.passivlingo.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or 
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
 """

from passivlingo_dictionary.models.SearchParam import SearchParam
from passivlingo_dictionary.helpers.SearchChainFactory import SearchChainFactory
from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper
from passivlingo_dictionary.wrappers.NltkWordNetWrapper import NltkWordNetWrapper
from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper
from passivlingo_dictionary.helpers.Constants import WORDNET_IDENTIFIER_OWN
from passivlingo_dictionary.helpers.Constants import WORDNET_IDENTIFIER_NLTK
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
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
        wrapperToUse = OwnWordNetWrapper(None) if wordnetId == WORDNET_IDENTIFIER_OWN else NltkWordNetWrapper(None)
        synset = wnToUse.synset(wrapperToUse.getWordKey(wordKey))

        result = []
        for item in synset.examples():
            result.append(item.replace('"', ''))

        return result
    
    def __repr__(self):
        return 'Dictionary()'
    def __str__(self):    
        return 'Dictionary()'
        

