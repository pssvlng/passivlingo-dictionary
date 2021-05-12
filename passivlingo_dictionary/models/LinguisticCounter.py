class LinguisticCounter:
    def __init__(self):
        self.antonym = 0
        self.hypernym = 0
        self.hyponym = 0
        self.holonym = 0  
        self.meronym = 0 
        self.entailment = 0
        self.mt = 0 #Machine Translation

    def add(self, counter):
        self.antonym += counter.antonym
        self.hypernym += counter.hypernym
        self.hyponym += counter.hyponym
        self.holonym += counter.holonym
        self.meronym += counter.meronym
        self.entailment += counter.entailment
        self.mt += counter.mt
        
        return self

    def __repr__(self):
        return 'LinguisticCounter()'
    def __str__(self):        
        return 'LinguisticCounter()'