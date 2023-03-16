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

from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam
from textblob import TextBlob

param = SearchParam()
dict = Dictionary()
#param.filterLang = 'europe'
param.woi = 'houses'
result = dict.findWords(param)
print(result)

#blob = TextBlob(param.woi)                        
#print(blob.detect_language())
