import os

print('installing nltk wordnet data ...')
os.system('python3 -m nltk.downloader wordnet')
print('installing nltk auxiliary libraries ...')
os.system('python3 -m nltk.downloader omw')
os.system('python3 -m nltk.downloader stopwords')