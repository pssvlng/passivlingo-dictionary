from passivlingo_dictionary.searchChains.CategorySearchChain import CategorySearchChain
from passivlingo_dictionary.searchChains.DefaultSearchChain import DefaultSearchChain
from passivlingo_dictionary.searchChains.LemmaSearchChain import LemmaSearchChain
from passivlingo_dictionary.searchChains.MtSearchChain import MtSearchChain
from passivlingo_dictionary.searchChains.WordKeySearchChain import WordKeySearchChain
from passivlingo_dictionary.searchChains.PosSearchChain import PosSearchChain
from passivlingo_dictionary.searchChains.ContainerSearchChain import ContainerSearchChain
from passivlingo_dictionary.searchChains.SearchChain import SearchChain
from passivlingo_dictionary.translationProviders.EmptyTranslationProvider import EmptyTranslationProvider
from passivlingo_dictionary.translationProviders.GoogleTranslationProvider import GoogleTranslationProvider
from passivlingo_dictionary.translationProviders.TextBlobTranslationProvider import TextBlobTranslationProvider 
from passivlingo_dictionary.helpers.CommonHelper import CommonHelper
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS_OWN
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP
from passivlingo_dictionary.helpers.Constants import NLTK_TO_OWN_LANGMAP_EXCLUSIONS
from passivlingo_dictionary.helpers.Constants import OWN_TO_NLTK_LANGMAP
from passivlingo_dictionary.helpers.Constants import OWN_TO_NLTK_LANGMAP_EXCLUSIONS
from passivlingo_dictionary.helpers.Constants import WORDNET_IDENTIFIER_NLTK
from passivlingo_dictionary.wrappers.OwnWordNetWrapper import OwnWordNetWrapper
from passivlingo_dictionary.wrappers.NltkWordNetWrapper import NltkWordNetWrapper
from passivlingo_dictionary.wrappers.WordNetWrapper import WordNetWrapper
from passivlingo_dictionary.models.SearchParam import SearchParam

class SearchChainFactory:        
    
    def getSearchChains(self, searchParam: SearchParam) -> []:
        
        if searchParam.wordkey is None and searchParam.woi is None:
            raise ValueError("Invalid argument list: 'woi' or 'wordkey' required")

        translationProvider = self.__getTranslationProvider(searchParam)                
        results = []
        
        if searchParam.filterLang:
            searchParam.filterLang = searchParam.filterLang.replace(" ", "")

        langDetails = self.__getWordNetLangDetails(searchParam.filterLang, searchParam.wordnetId)
        if (searchParam.filterLang and len(langDetails[0]) != 0) or not searchParam.filterLang:
            wordNetWrapper = self.__getWordNetWrapper(','.join(langDetails[0]), searchParam.wordnetId)
            wordNetLangs = VALID_WORDNET_LANGS if searchParam.wordnetId == WORDNET_IDENTIFIER_NLTK else VALID_WORDNET_LANGS_OWN        
            results.append(self.__getSearchChain(wordNetWrapper, wordNetLangs, translationProvider, searchParam, ','.join(langDetails[0])))
                
        if len(langDetails[1]) > 0:        
            additionalSearchChains = self.__getAdditionalSearchChains(searchParam.wordnetId, langDetails[1], translationProvider, searchParam)
            for item in additionalSearchChains:
                results.append(item)

        return results
                                          
    def __getSearchChain(self, wordNetWrapper, wordNetLangs, translationProvider, searchParam: SearchParam, filterLangs) -> SearchChain:        
        if searchParam.wordkey is not None:            
            if self.__isMtSearchChain(filterLangs, wordNetLangs):
                return self.__getMtSearchChain(searchParam.wordkey.split('.')[0], filterLangs, wordNetWrapper, translationProvider)
            elif self.__isWordKeySearchChain(searchParam.lang, searchParam.category, searchParam.woi, searchParam.lemma, searchParam.pos):                                   
                return self.__getWordKeySearchChain(searchParam.wordkey, searchParam.category, searchParam.lang, filterLangs, wordNetWrapper, translationProvider)
            else:
                raise ValueError("Invalid argument list: 'wordkey', 'lang' and 'category' required")                    

        if searchParam.woi is not None:            
            if self.__isMtSearchChain(filterLangs, wordNetLangs):
                return self.__getMtSearchChain(searchParam.woi, filterLangs, wordNetWrapper, translationProvider)    
            elif self.__isDefaultSearchChain(searchParam.category, searchParam.lang, searchParam.lemma, searchParam.pos):              
                return self.__getDefaultSearchChain(searchParam.woi, filterLangs, wordNetWrapper, translationProvider)
            elif self.__isCategorySearchChain(searchParam.lang, searchParam.category, searchParam.lemma, searchParam.pos):                
                return self.__getCategorySearchChain(searchParam.woi, searchParam.lang, searchParam.category, filterLangs, wordNetWrapper, translationProvider)
            elif self.__isPosSearchChain(searchParam.lang, searchParam.lemma, searchParam.pos, searchParam.category):                        
                return self.__getPosSearchChain(searchParam.woi, searchParam.lang, searchParam.lemma, searchParam.pos, filterLangs, wordNetWrapper, translationProvider)
            else:
                raise ValueError('Invalid argument list, possible combinations: (woi), (wordkey, lang, category), (woi, lang, category), (woi, lang, pos, lemma)')                        

    def __getTranslationProvider(self, searchParam: SearchParam):
        if searchParam.googleApiKey:
            return GoogleTranslationProvider(searchParam.googleApiKey)

        return EmptyTranslationProvider()

    def __getWordNetWrapper(self, filterLang, wordnetId) -> WordNetWrapper:        
        return NltkWordNetWrapper(filterLang) if wordnetId == WORDNET_IDENTIFIER_NLTK else OwnWordNetWrapper(filterLang)

    def __getWordNetLangDetails(self, filterLang, wordnetId):
        if not filterLang:
            return ([], [])
        langList = filterLang.split(',')
        removeList = []
        validLangs = VALID_WORDNET_LANGS_OWN
        langMap = NLTK_TO_OWN_LANGMAP
        exclusionLangMap = NLTK_TO_OWN_LANGMAP_EXCLUSIONS
        if wordnetId == WORDNET_IDENTIFIER_NLTK:
            validLangs = VALID_WORDNET_LANGS
            langMap = OWN_TO_NLTK_LANGMAP
            exclusionLangMap = OWN_TO_NLTK_LANGMAP_EXCLUSIONS
        
        result = []
        for lang in langList:
            try:
                result.append(CommonHelper.getWordnetLanguageCode(lang, validLangs, langMap)) 
            except ValueError:
                if lang not in exclusionLangMap:
                    removeList.append(lang)
                else:
                    result.append(lang)    
        
        return (result, removeList)        

    def __getAdditionalSearchChains(self, wordnetId, deltaList, translationProvider, searchParam: SearchParam) -> []:
        result = []
        if len(deltaList) > 0:
            if wordnetId != WORDNET_IDENTIFIER_NLTK:
                result.append(self.__getSearchChain(NltkWordNetWrapper(','.join(deltaList)), VALID_WORDNET_LANGS, translationProvider, searchParam, ','.join(deltaList)))                
            else:
                result.append(self.__getSearchChain(OwnWordNetWrapper(','.join(deltaList)), VALID_WORDNET_LANGS, translationProvider, searchParam, ','.join(deltaList)))                
                
        return result    

    def __isWordKeySearchChain(self, lang, category, woi, lemma, pos) -> bool:
        return all(x is not None for x in [lang, category]) and all(x is None for x in [woi, lemma, pos])

    def __getWordKeySearchChain(self, wordkey, category, lang, filterLang, wordNetWrapper, translationProvider) -> SearchChain:
        wordkeyArr = wordkey.split('.')        
        items = [WordKeySearchChain(category, wordkey, lang, wordNetWrapper), MtSearchChain(translationProvider, wordkeyArr[0], lang, filterLang)]        
        return ContainerSearchChain(items, wordkeyArr[0], lang, wordNetWrapper)
    
    def __isMtSearchChain(self, filterLang, wordNetLangs) -> bool:
        langVariants = CommonHelper.getLangVariant(filterLang)        
        return filterLang and all(x not in langVariants for x in wordNetLangs) and len(filterLang.split(',')) == 1        

    def __getMtSearchChain(self, woi, filterLang, wordNetWrapper, translationProvider) -> SearchChain:
        woi = CommonHelper.sanatizeWord(woi)    
        items = [MtSearchChain(translationProvider, woi, None, filterLang)]
        return  ContainerSearchChain(items, woi, None, wordNetWrapper)

    def __isDefaultSearchChain(self, category, lang, lemma, pos) -> bool:
        return all(x is None for x in [category, lang, lemma, pos])

    def __getDefaultSearchChain(self, woi, filterLang, wordNetWrapper, translationProvider) -> SearchChain:
        woi = CommonHelper.sanatizeWord(woi)    
        items = [DefaultSearchChain(woi, None, wordNetWrapper), LemmaSearchChain(woi, None, wordNetWrapper), MtSearchChain(translationProvider, woi, None, filterLang)]         
        return  ContainerSearchChain(items, woi, None, wordNetWrapper)
    
    def __isCategorySearchChain(self, lang, category, lemma, pos) -> bool:
        return all(x is not None for x in [lang, category]) and all(x is None for x in [lemma, pos])

    def __getCategorySearchChain(self, woi, lang, category, filterLang, wordNetWrapper, translationProvider) -> SearchChain:        
        woi = CommonHelper.sanatizeWord(woi)
        items = [CategorySearchChain(category, woi, lang, wordNetWrapper), DefaultSearchChain(woi, lang, wordNetWrapper), LemmaSearchChain(woi, lang, wordNetWrapper), MtSearchChain(translationProvider, woi, lang, filterLang)]        
        return ContainerSearchChain(items, woi, lang, wordNetWrapper)
    
    def __isPosSearchChain(self, lang, lemma, pos, category) -> bool:
        return all(x is not None for x in [lang, lemma, pos]) and category is None

    def __getPosSearchChain(self, woi, lang, lemma, pos, filterLang, wordNetWrapper, translationProvider) -> SearchChain:
        woi = CommonHelper.sanatizeWord(woi)
        items = [PosSearchChain(pos, lemma, lang, wordNetWrapper), DefaultSearchChain(woi, lang, wordNetWrapper), MtSearchChain(translationProvider, woi, lang, filterLang)]        
        return ContainerSearchChain(items, woi, lang, wordNetWrapper)   
