import json

from .definition import Definition


class DictionaryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Dictionary):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)

class Dictionary:
    def __init__(self, name):
        self.name = name
        self.dict: list[Definition] = list()

    def __contains__(self, word):
        for defn in self.dict:
            if defn.word.word == word:
                return True
        return False
    
    def __len__(self):
        return len(self.dict)
    
    def __iter__(self):
        for defn in self.dict:
            yield defn

    def __str__(self):
        o = ''
        pad = len(str(len(self)))
        for i, defn in enumerate(sorted(self.dict)):
            o += (' ' * (pad - len(str(i+1)))) + f'{i+1}. {defn}\n'
        return o

    def __getitem__(self, word):
        for defn in self.dict:
            if defn.word == word:
                return defn
            
    def to_dict(self):
        d = {'name': self.name, 'definitions': []}
        for defn in self.dict:
            d['definitions'].append(defn.to_dict())
        return d

    def info(self):
        print('Name: ' + self.name)
        print('# of words: ' + str(len(self)))

    def add(self, definition: Definition):
        self.dict.append(definition)