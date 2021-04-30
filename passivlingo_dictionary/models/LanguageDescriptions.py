class LanguageDescriptions:
    def __init__(self):
        self.english = ''
        self.spanish = ''
        self.french = ''
        self.german = ''
        self.portuguese = ''
        self.italian = ''        
        self.dutch = ''        

    def getWordDescription(self, lang):
        if lang in ['fra', 'fr']:
            return self.french
        if lang in ['spa', 'es']:
            return self.spanish
        if lang in ['por', 'pt']:
            return self.portuguese             
        if lang in ['ita', 'it']:
            return self.italian            
        if lang in ['eng', 'en']:
            return self.english            
        if lang in ['ger', 'de']:
            return self.german            
        if lang in ['nld', 'nl']:
            return self.dutch                    

        return ''    

    def setWordDescription(self, lang, woi):        
        if lang in ['fra', 'fr']:
            self.french = woi
            return
        if lang in ['spa', 'es']:
            self.spanish = woi
            return
        if lang in ['por', 'pt']:
            self.portuguese = woi
            return    
        if lang in ['ita', 'it']:
            self.italian = woi
            return
        if lang in ['eng', 'en']:
            self.english = woi
            return            
        if lang in ['ger', 'de']:
            self.german = woi
            return
        if lang in ['nld', 'nl']:
            self.dutch = woi
            return    
        return

    def getWordDescriptions(self, separator):
        return separator.join([self.french, self.spanish, self.portuguese, self.italian, self.english, self.german, self.dutch])        


        