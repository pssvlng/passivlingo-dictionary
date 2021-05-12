import pyttsx3
import sys
from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam
#debian linux: sudo apt install espeak
#windows: pip3 install pypiwin32
#mac? 

DEBIAN_LOOKUP = {
    "als":"albanian",
    "arb":"arabic",
    "bg":"bulgarian",
    "ca":"catalan",
    "de":"german",
    "da":"danish",
    "el":"greek",
    "en":"english",
    "es":"spanish",
    "eu":"default",
    "fi":"finnish",
    "fr":"french",
    "gl":"default",
    "he":"default",
    "hr":"croatian",
    "id":"indonesian",
    "it":"italian",
    "jp":"japanese",
    "nb":"norwegian",
    "nn":"norwegian",        
    "nl":"dutch",
    "pl":"polish",
    "pt":"portuguese",
    "sk":"slovak",
    "sl":"slovenian",
    "sv":"swedish",
    "th":"default",
    "zh":"Mandarin",
    "zsm":"malay",
    "ro":"rominian",
    "is":"icelandic",
    "lt":"lithuanian",
    "fas":"persian",
    "fa":"persian",
    "af":"afrikaans",
} 

def main(argv):
    mydict = Dictionary()
    searchParam = SearchParam()
    argvTransform = {}    
   
    for item in argv:
        key, value = item.split("=", 1)
        argvTransform[key] = value
    
    lang = DEBIAN_LOOKUP.get(argvTransform['lang'], 'default')
    engine = pyttsx3.init()
    engine.setProperty('voice', lang)
    engine.setProperty('rate', 120)
    engine.say(argvTransform['text'].replace("_", " "))
    engine.runAndWait()    
    
    print("OK")

if __name__ == "__main__":
   main(sys.argv[1:])
   


