from .Lemmatizer import Lemmatizer

class DefaultLemmatizer(Lemmatizer):

    def lemmatize(self, woi):
        return [woi]
        