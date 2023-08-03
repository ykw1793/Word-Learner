from .word import Word, Meaning

class Definition:
    def __init__(self, word: Word, meanings: list[Meaning] = None):
        self.word = word
        if meanings is None:
            self.meanings = []
        else:
            self.meanings = meanings

    def __hash__(self):
        return hash(self.word)
    
    def __str__(self):
        o = f'\033[4m{self.word}\033[0m\n'
        for i in range(len(self.meanings)):
            o += (' ' * 2) + f'{i+1}. {self.meanings[i]}\n'
        return o
    
    def __lt__(self, obj):
        return self.word < obj.word
    
    def to_dict(self):
        d = {'word': self.word.word, 'meanings': []}
        for meaning in self.meanings:
            d['meanings'].append(str(meaning))
        return d
    
    def add_meaning(self, meaning):
        self.meanings.append(meaning)