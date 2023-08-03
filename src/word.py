from typing import Type

from .pos import Pos

class Meaning:
    def __init__(self, _type: Pos, meaning: str):
        self.type = _type
        self.meaning = meaning

    def __str__(self):
        return f'({str(self.type).replace("Pos.", "")}) {self.meaning}' 


class Word:
    def __init__(self, word: str):
        self.word = word

    def __hash__(self):
        return hash(self.word)
    
    def __len__(self):
        return len(self.word)
    
    def __str__(self):
        return self.word
    
    def __lt__(self, obj):
        return self.word < obj.word
    
    def __eq__(self, obj):
        if type(obj) == str:
            return self.word == obj
        elif type(obj) == Word:
            return self.word == obj.word

