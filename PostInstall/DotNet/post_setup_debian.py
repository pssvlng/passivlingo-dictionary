import os
import spacy
from spacy.cli.download import download

def install(lang):
    try:
        download(model=lang)
    except BaseException as e:  
        print(str(e))      

print('Installing spaCy data sets. This can take a while ...')        
install("en_core_web_sm")
install("fr_core_news_sm")
install("es_core_news_sm")
install("it_core_news_sm")
install("nl_core_news_sm")
install("pt_core_news_sm")
install("de_core_news_sm")
install("da_core_news_sm")
install("el_core_news_sm")
install("ja_core_news_sm")
install("lt_core_news_sm")
install("nb_core_news_sm")
install("pl_core_news_sm")
install("ro_core_news_sm")

try:
    os.system('sudo apt update && sudo apt install espeak ffmpeg libespeak1')
except BaseException as e:  
    print(str(e))      
