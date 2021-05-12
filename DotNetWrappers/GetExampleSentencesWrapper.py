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
        'wordnetid': None,              
    }
   
    for item in argv:
        key, value = item.split("=", 1)
        argvTransform[key] = value
        
    argvTransform['wordkey'] = argvTransform['wordkey'].replace("_", " ")    
        
    results = mydict.getExampleSentences(argvTransform['wordkey'], argvTransform['wordnetid'])
    print(WordEncoder().encode(results))

if __name__ == "__main__":
   main(sys.argv[1:])


