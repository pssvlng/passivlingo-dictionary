import wn, sys, tempfile, os
from passivlingo_dictionary.encoders.WordEncoder import WordEncoder
from passivlingo_dictionary.wrappers.OwnSynsetWrapper import OwnSynsetWrapper
from pathlib import Path
from ImageWrapper import getArgvTransform
from ImageWrapper import writeOutput
from ImageWrapper import formatNodeDisplay

def main(argv):
            
    try:

        argvTransform = getArgvTransform(argv)

        dotFilePath = os.path.sep.join([tempfile.gettempdir(), f"{argvTransform['fileName']}.dot"])
        pngFilePath = os.path.sep.join([tempfile.gettempdir(), f"{argvTransform['fileName']}.png"])
        data = {"result": True, "filePath": pngFilePath, "msg": "Success"}

        if Path(pngFilePath).is_file():
            print(WordEncoder().encode(data))
            return

        synset = OwnSynsetWrapper(None, wn.synset(argvTransform['synsetId']))
        level = int(argvTransform['level'])
        branch_count = int(argvTransform['maxLeafNodes'])
        filter_langs = argvTransform['filterLangs']
        ili = argvTransform['ili']
        synonym_count = int(argvTransform['synonymCount'])

        body = f'{buildgraph_body(synset, level, filter_langs, ili, synonym_count, branch_count, True)}{buildgraph_body(synset, level, filter_langs, ili, synonym_count, branch_count, False)}'
        partwhole_template = '''graph g {
            rankdir=RL
            "{root0}" [shape=box, style=bold]
            node [shape = box,height=.1];
            {body}
        }'''

        root = formatNodeDisplay(synset, filter_langs, ili, synonym_count)    
        writeOutput(partwhole_template, root, body, dotFilePath, pngFilePath, data)

    except Exception as e:
        repr_ = getattr(e, 'message', repr(e))
        str_ = getattr(e, 'message', str(e))
        data = {"result": False, "filePath": pngFilePath, "msg": f'repr: {repr_}, str: {str_}'}  
        print(WordEncoder().encode(data))        
    
def buildgraph_body(synset, level, filter_langs, ili, synonym_count, branch_count, build_up):
    if level == 0:
        return ''

    if build_up: 
        branches = synset.holonyms()
    else:
        branches = synset.meronyms()

    root = formatNodeDisplay(synset, filter_langs, ili, synonym_count)    
    entry = ''
    returnstr = ''
    for item in branches[:branch_count]:
        itemDisplay = formatNodeDisplay(item, filter_langs, item.ili, synonym_count)
        if build_up:      
            entry = f'{entry}"{root}"--"{itemDisplay}";'
        else:    
            entry = f'{entry}"{itemDisplay}"--"{root}";'
        
        returnstr = f'{returnstr}{buildgraph_body(item, level-1, filter_langs, item.ili, synonym_count, branch_count, build_up)}' 

    return f'{entry}{returnstr}'    

if __name__ == "__main__":
   main(sys.argv[1:])
