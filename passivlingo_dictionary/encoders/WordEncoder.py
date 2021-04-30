from json import JSONEncoder

class WordEncoder(JSONEncoder):

    def default(self, object):
        return object.__dict__ 