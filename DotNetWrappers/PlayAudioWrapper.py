import pyttsx3
import sys
import os
import platform
import tempfile
from gtts import gTTS
from playsound import playsound
from passivlingo_dictionary.Dictionary import Dictionary
from passivlingo_dictionary.models.SearchParam import SearchParam

ESPEAK_LOOKUP = {
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
    "pt":"portugal",
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

GTTS_LOOKUP = {
    "als":"sq",
    "arb":"ar",
    "bg":"bg",
    "ca":"ca",
    "de":"de",
    "da":"da",
    "el":"el",
    "en":"en",
    "es":"es",
    "eu":"eu",
    "fi":"fi",
    "fr":"fr",
    "gl":"gl",
    "he":"he",
    "hr":"hr",
    "id":"id",
    "it":"it",
    "jp":"ja",
    "nb":"no",
    "nn":"no",        
    "nl":"nl",
    "pl":"pl",
    "pt":"pt",
    "sk":"sk",
    "sl":"sl",
    "sv":"sv",
    "th":"th",
    "zh":"zh",
    "zsm":"id",
    "ro":"ro",
    "is":"is",
    "lt":"lt",
    "fas":"fa",
    "fa":"fa",
    "af":"af",
}

def espeak(argvTransform):
    lang = ESPEAK_LOOKUP.get(argvTransform['lang'], 'default')
    engine = pyttsx3.init()
    if (platform.system() == 'Windows'):
        engine = pyttsx3.init('sapi5')
    
    engine.setProperty('voice', lang)
    engine.setProperty('rate', 120)
    engine.say(argvTransform['text'].replace("_", " "))
    engine.runAndWait()    

def runGtts(argvTransform):
    lang = GTTS_LOOKUP.get(argvTransform['lang'], 'en')    
    tts = gTTS(argvTransform['text'].replace("_", " "), lang=lang)
    file = os.path.sep.join([tempfile.gettempdir(), f"{argvTransform['text']}.mp3"])
    tts.save(file)
    playsound(file)    

def main(argv):
    mydict = Dictionary()
    searchParam = SearchParam()
    argvTransform = {}    
   
    for item in argv:
        key, value = item.split("=", 1)
        argvTransform[key] = value
    
    try:
        runGtts(argvTransform)
    except:
        espeak(argvTransform)
    
    print("OK")

if __name__ == "__main__":
   main(sys.argv[1:])
   


