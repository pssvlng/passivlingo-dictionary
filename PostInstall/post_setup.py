
from spacy.cli.download import download
import os
import wn

def installOwn():
    print('Installing OWN data set: English ...')
    wn.download('ewn:2020')
    print('Installing OWN data set: German ...')
    wn.download('odenet:1.3')
    print('Installing OWN data set: Albanian ...')
    wn.download('alswn:1.3+omw')
    print('Installing OWN data set: Arabic ...')
    wn.download('arbwn:1.3+omw')
    print('Installing OWN data set: Bulgarian ...')
    wn.download('bulwn:1.3+omw')
    print('Installing OWN data set: Chinese ...')
    wn.download('cmnwn:1.3+omw')
    print('Installing OWN data set: Croatian ...')
    wn.download('hrvwn:1.3+omw')
    print('Installing OWN data set: Danish ...')
    wn.download('danwn:1.3+omw')
    print('Installing OWN data set: Finnish ...')
    wn.download('finwn:1.3+omw')
    print('Installing OWN data set: Greek ...')
    wn.download('ellwn:1.3+omw')
    print('Installing OWN data set: Hebrew ...')
    wn.download('hebwn:1.3+omw')
    print('Installing OWN data set: Islandic ...')
    wn.download('islwn:1.3+omw')
    print('Installing OWN data set: Italian ...')
    wn.download('itawn:1.3+omw')
    print('Installing OWN data set: Japanese ...')
    wn.download('jpnwn:1.3+omw')
    print('Installing OWN data set: Lithuanian ...')
    wn.download('litwn:1.3+omw')
    print('Installing OWN data set: Catalonian ...')
    wn.download('catwn:1.3+omw')
    print('Installing OWN data set: Basque ...')
    wn.download('euswn:1.3+omw')
    print('Installing OWN data set: Galacian ...')
    wn.download('glgwn:1.3+omw')
    print('Installing OWN data set: Spanish ...')
    wn.download('spawn:1.3+omw')
    print('Installing OWN data set: Norwegian ...')
    wn.download('nobwn:1.3+omw')
    wn.download('nnown:1.3+omw')
    print('Installing OWN data set: Dutch ...')
    wn.download('nldwn:1.3+omw')
    print('Installing OWN data set: Portuguese ...')
    wn.download('porwn:1.3+omw')
    print('Installing OWN data set: Polish ...')
    wn.download('polwn:1.3+omw')
    print('Installing OWN data set: Rominian ...')
    wn.download('ronwn:1.3+omw')
    print('Installing OWN data set: Slovinian ...')
    wn.download('slkwn:1.3+omw')
    print('Installing OWN data set: Slovakian ...')
    wn.download('slvwn:1.3+omw')
    print('Installing OWN data set: Swedish ...')
    wn.download('swewn:1.3+omw')
    print('Installing OWN data set: Thai ...')
    wn.download('thawn:1.3+omw')
    print('Installing OWN data set: French ...')
    wn.download('frawn:1.3+omw')
    print('Installing OWN data set: Indonesian ...')
    wn.download('indwn:1.3+omw')
    print('Installing OWN data set: Malaysian ...')
    wn.download('zsmwn:1.3+omw')

def installNltk():
    print('installing nltk wordnet data ...')
    os.system('python3 -m nltk.downloader wordnet')
    print('installing nltk auxiliary libraries ...')
    os.system('python3 -m nltk.downloader omw')
    os.system('python3 -m nltk.downloader stopwords')
    #Could possibly also be done with nltk.download('all') or nltk.download() for user interaction        

def install(lang):
    try:
        download(model=lang)
    except BaseException as e:  
        print(str(e))  

def installSpacy():
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

print('Running post installation scripts ...')                       

print('Installing OWN language data sets. This can take a while ...')
installOwn()

print('Installing NLTK data sets. This can take a while ...')        
installNltk()

print('Installing spaCy data sets. This can take a while ...')        
installSpacy()

         