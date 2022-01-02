import os, wn
from passivlingo_dictionary.encoders.WordEncoder import WordEncoder
from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper

def getArgvTransform(argv):
    if len(argv) < 3:
        raise ValueError('Program expects at least 3 arguments')
        
    argvTransform = {
        'fileName': None,
        'level': None,
        'filterLangs': None,
        'maxLeafNodes': None,
        'ili': None,
        'synonymCount': None,
        'synsetId': None        
    }

    for item in argv:
        key, value = item.split("=", 1)
        argvTransform[key] = value

    return argvTransform    

def writeOutput(template, root, body, dotFilePath, pngFilePath, result):
    fileText = template.replace('{root0}', root)
    fileText = fileText.replace('{body}', body)
    
    with open(dotFilePath, 'w') as file:
        file.write(fileText)
    
    os.system(f'dot -Tpng {dotFilePath} -o {pngFilePath}')
    print(WordEncoder().encode(result))     

def formatSynonymDisplay(synset, synonym_count):
    lemmas = synset.lemmas()
    result = ''

    if synset.id != '*INFERRED*':
        result = lemmas[0]
        for synonym in lemmas[1:synonym_count]:
            result += f',{synonym}'

    return f'{result}{{{synset.pos}}}'

def formatNodeDisplay(synset, filter_langs, ili, synonym_count):
    
    result = {}
    if filter_langs and ili:        
        for lang in filter_langs.split(','):
            synsets_local = wn.synsets(ili=ili, lang=lang)
            if len(synsets_local) > 0:
                s = OwnSynsetWrapper(None, synsets_local[0])
                result[lang] = formatSynonymDisplay(s, synonym_count)            
    else:        
        result[synset.id] = formatSynonymDisplay(synset, synonym_count)

    if len(result) == 0:
        s = OwnSynsetWrapper(None, wn.synsets(ili=ili, lang='en')[0])
        result['en'] = formatSynonymDisplay(s, synonym_count)

    return f"{'|'.join(result.values())}"