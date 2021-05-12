import sys, getopt, json
from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam
from passivlingo_dictionary.encoders.WordEncoder import WordEncoder
from types import SimpleNamespace

def main(argv):
    mydict = Dictionary()
    searchParam = SearchParam()
    argvTransform = {}

    argvTransform = {
        'wordkey': None,
        'category': None,
        'lang': None,
        'woi': None,
        'lemma': None,
        'pos': None,
        'filterLang': None,
        'wordnetId': None,      
        'googleApiKey': None,
        'ili': None         
    }
   
    for item in argv:
        key, value = item.split("=", 1)
        argvTransform[key] = value
    
    if argvTransform['wordnetId'] != 'nltk' and argvTransform['woi']:
        argvTransform['woi'] = argvTransform['woi'].replace("_", " ")    
    
    searchParam = json.loads(json.dumps(argvTransform), object_hook=lambda d: SimpleNamespace(**d))   
    results = mydict.findWords(searchParam)
    print(WordEncoder().encode(results))

if __name__ == "__main__":
   main(sys.argv[1:])


