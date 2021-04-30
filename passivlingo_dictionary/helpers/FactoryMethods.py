from passivlingo_dictionary.extractors.AntonymExtractor import AntonymExtractor
from passivlingo_dictionary.extractors.HypernymExtractor import HypernymExtractor
from passivlingo_dictionary.extractors.HyponymExtractor import HyponymExtractor
from passivlingo_dictionary.extractors.HolonymExtractor import HolonymExtractor
from passivlingo_dictionary.extractors.MeronymExtractor import MeronymExtractor
from passivlingo_dictionary.extractors.EntailmentExtractor import EntailmentExtractor
from passivlingo_dictionary.extractors.AdjectiveExtractor import AdjectiveExtractor
from passivlingo_dictionary.extractors.PosExtractor import PosExtractor
from passivlingo_dictionary.extractors.CombinedExtractor import CombinedExtractor
from passivlingo_dictionary.lemmatizers.DefaultLemmatizer import DefaultLemmatizer
from passivlingo_dictionary.lemmatizers.SpacyLemmatizer import SpacyLemmatizer
from passivlingo_dictionary.tokenizers.GenericTokenizer import GenericTokenizer
from passivlingo_dictionary.posTaggers.SpacyPosTagger import SpacyPosTagger
from urllib.parse import unquote
from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS
from passivlingo_dictionary.helpers.Constants import VALID_WORDNET_LANGS_OWN

class FactoryMethods:        

    @classmethod
    def getTokenizer(cls, sent, lang):
        return GenericTokenizer(unquote(sent), lang, SpacyPosTagger(lang))    
        
    @classmethod
    def getLemmatizer(cls, lang):
        if lang in (VALID_WORDNET_LANGS + VALID_WORDNET_LANGS_OWN):
            return SpacyLemmatizer(lang)

        return DefaultLemmatizer()            

    @classmethod
    def getExtractor(cls, category, wordNetWrapper):
        choices = {'antonym': AntonymExtractor(wordNetWrapper), 'hypernym': HypernymExtractor(wordNetWrapper), 'hyponym': HyponymExtractor(wordNetWrapper), 'holonym': HolonymExtractor(wordNetWrapper), 'meronym' : MeronymExtractor(wordNetWrapper), 'entailment': EntailmentExtractor(wordNetWrapper)}
        return choices.get(category, None)                    

    @classmethod
    def getExtractorByPos(cls, pos, wordNetWrapper):    
        choices = {'v': PosExtractor(wordNetWrapper, 'v'), 'n': PosExtractor(wordNetWrapper, 'n'), 'a': AdjectiveExtractor(wordNetWrapper), 'r': PosExtractor(wordNetWrapper, 'r')}
        return choices.get(pos, CombinedExtractor(wordNetWrapper))

    @classmethod
    def getOwnSynsetWrappers(cls, synsets, lang):
        result = []
        for synset in synsets:
            result.append(OwnSynsetWrapper(lang, synset))

        return result            
