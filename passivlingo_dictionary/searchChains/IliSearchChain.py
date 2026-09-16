from .SearchChain import SearchChain

class IliSearchChain(SearchChain):

    def __init__(self, ili, lang, wordNetWrapper):
        super().__init__('', lang)
        self.ili = ili
        self.wordNetWrapper = wordNetWrapper

    def execute(self):
        lang = self.wordNetWrapper.getWordnetLanguageCode(self.lang)
        return self.wordNetWrapper.getWordsFromIli(self.ili, lang)

    def __repr__(self):
        return f'IliSearchChain({self.woi} {repr(self.wordNetWrapper)})'