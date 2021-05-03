import nltk
from urllib.parse import unquote
from passivlingo_dictionary.helpers.FactoryMethods import FactoryMethods

class TextProcessor:

    def tokenizeParagraph(self, paragraph: str):
        if paragraph is None:
            raise ValueError("Invalid argument list: 'paragraph' required")

        paragraph = unquote(paragraph)
        return nltk.sent_tokenize(paragraph)

    def tokenizeSentence(self, sentence: str, lang: str):
        if None in [sentence, lang]:
            raise ValueError("Invalid argument list: 'lang' and 'sent' required")
        
        sentence = unquote(sentence)
        tokenizer = FactoryMethods.getTokenizer(sentence, lang)
        return tokenizer.tokenize()
    
    def __repr__(self):
        return 'TextProcessor()'
    def __str__(self):    
        return 'TextProcessor()'
            