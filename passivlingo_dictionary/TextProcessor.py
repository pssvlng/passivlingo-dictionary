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
            