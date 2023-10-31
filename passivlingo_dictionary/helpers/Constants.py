VALID_WORDNET_LANGS = ['als', 'arb', 'bul', 'cat', 'cmn', 'dan', 'ell', 'eng', 'eus', 'fas', 'fin', 'fra', 'glg', 'heb', 'hrv', 'ind', 'ita', 'jpn', 'nld', 'nno', 'nob', 'pol', 'por', 'qcn', 'slv', 'spa', 'swe', 'tha', 'zsm']
VALID_EU_LANGS = ['eng', 'fra', 'spa', 'ita', 'nld', 'por', 'ger', 'deu']

VALID_EU_LANGS_OWN = ['en', 'fr', 'es', 'it', 'nl', 'pt', 'de']
VALID_AFRICA_LANGS_OWN = ['am', 'bm', 'ny', 'dv', 'ee', 'gu', 'ha', 'ig', 'rw', 'kri', 'ln', 'lg', 'mg', 'om', 'nso', 'st', 'sn', 'so', 'sw', 'ti', 'ts', 'tw', 'xh', 'yo', 'zu']
VALID_WORDNET_LANGS_OWN = ['af', 'als', 'arb', 'bg', 'ca', 'da', 'el', 'eu', 'fi', 'gl', 'he', 'hr', 'id', 'is', 'jp', 'lt', 'nb', 'pl', 'ro', 'sk', 'sl', 'sv', 'th', 'ua', 'zh', 'zsm'] + VALID_EU_LANGS_OWN + VALID_AFRICA_LANGS_OWN

DOMAIN_NAMES = ['.co', '.de', '.nl', '.pt', '.es', '.org', '.net', '.fr', '.it', '.net', '.com', '.edu', '.gov']

WORDNET_IDENTIFIER_NLTK = 'nltk'
WORDNET_IDENTIFIER_OWN = 'own'

OWN_TO_NLTK_LANGMAP = {
    'als': 'als', 
    'arb': 'arb', 
    'bg': 'bul', 
    'ca': 'cat', 
    'da': 'dan',     
    'el': 'ell', 
    'en': 'eng', 
    'es': 'spa', 
    'eu': 'eus', 
    'fi': 'fin', 
    'fr': 'fra',     
    'gl': 'glg', 
    'he': 'heb', 
    'hr': 'hrv', 
    'id': 'ind',     
    'it': 'ita', 
    'jp': 'jpn',     
    'nb': 'nob', 
    'nl': 'nld', 
    'pl': 'pol', 
    'pt': 'por',         
    'sl': 'slv', 
    'sv': 'swe', 
    'th': 'tha', 
    'zh': 'cmn', 
    'zsm': 'zsm'
}

OWN_TO_NLTK_LANGMAP_EXCLUSIONS = {
    'fa': 'fas', 
    'de': 'deu',
    'is': 'isl',
    'ro': 'ron',
    'sk': 'slk',
    'lt': 'lit',
    'af': 'afr',
    'ua': 'ukr'
} 

NLTK_TO_OWN_LANGMAP = {
    'als': 'als',
    'arb': 'arb', 
    'bul': 'bg', 
    'cat': 'ca', 
    'cmn': 'zh', 
    'dan': 'da', 
    'ell': 'el', 
    'eng': 'en', 
    'eus': 'eu',     
    'fin': 'fi', 
    'fra': 'fr',     
    'glg': 'gl', 
    'heb': 'he', 
    'hrv': 'hr', 
    'ind': 'id', 
    'ita': 'it', 
    'jpn': 'jp', 
    'nld': 'nl', 
    'nno': 'nb', 
    'nob': 'nb', 
    'pol': 'pl', 
    'por': 'pt',     
    'slv': 'sl', 
    'spa': 'es', 
    'swe': 'sv', 
    'tha': 'th', 
    'zsm': 'zsm'
}

NLTK_TO_OWN_LANGMAP_EXCLUSIONS = {
    'fas': 'fa', 
    'deu': 'de',
    'ger': 'de',
    'isl': 'is',
    'ron': 'ro',
    'slk': 'sk',
    'lit': 'lt',
    'afr': 'af',
    'ukr': 'ua'
}
