import cmd
import os
import json
import shutil

from src.dictionary import Dictionary, DictionaryEncoder
from src.definition import Definition
from src.word import Word, Meaning
from src.pos import Pos

class Shell(cmd.Cmd):
    intro = 'Welcome to word-learner shell. Type help or ? to list commands.\n'
    prompt = '(word) '
    dictionary = None
    file = None

    def dict_exists(self):
        if self.dictionary is None:
            print('\nNo dictionary loaded.\n')
            return False
        return True

    def do_create(self, arg):
        arg = arg.split()
        if len(arg) == 1:
            self.dictionary = Dictionary(arg[0])
            print('\nCreated new dictionary named \"' + arg[0] + '\".\n')
        else:
            self.default('\"create\" needs to be followed by dictionary name.')

    def do_add(self, arg):
        if self.dict_exists():
            print('\nAdd new word to dictionary \"' + self.dictionary.name + '\"')
            print('-' * os.get_terminal_size().columns)
            exit_status = False
            while True:
                word = input('Word ("-" to quit): ')
                if word == '':
                    print('Invalid input. Please try again.')
                    continue
                elif word == '-':
                    print('No new definition added.')
                    exit_status = True
                word = Word(word)
                break
            if exit_status == False: 
                defn = Definition(word)
                print('Meanings: ')
                i = 1
                while True:
                    pos = input(f'{i}. Part of speech (n/adj/v/adv or "-" to finish): ')
                    if pos == '-':
                        break
                    elif pos.lower() == 'n':
                        pos = Pos.n
                    elif pos.lower() == 'adj':
                        pos = Pos.adj
                    elif pos.lower() == 'v':
                        pos = Pos.v
                    elif pos.lower() == 'adv':
                        pos = Pos.adv
                    else:
                        print('Invalid input. Please try again.')
                        continue
                    mng = input((' ' * (len(str(i)) + 2)) + 'Meaning: ')
                    meaning = Meaning(pos, mng)
                    defn.add_meaning(meaning)
                    print(defn)
                    i += 1
                if len(defn.meanings) == 0:
                    print('Word not defined. No new definition added.')
                else:
                    self.dictionary.add(defn)
                    print(f'Added word "{defn.word}" to dictionary "{self.dictionary.name}"')
            print('-' * os.get_terminal_size().columns + '\n')

    def do_define(self, arg):
        if self.dict_exists():
            postcmd = arg.split()
            if len(postcmd) == 1:
                word = postcmd[0]
                if word in self.dictionary:
                    print()
                    print(self.dictionary[word])
                    print()
            else:
                self.default(arg)

    def do_info(self, arg):
        if self.dict_exists():
            print()
            self.dictionary.info()
            print()

    def do_list(self, arg):
        postcmd = arg.split()
        if self.dict_exists():
            if postcmd[0] == 'all':
                print('\nListing all definitions in dictionary \"' 
                      + self.dictionary.name + '\".')
                print('-' * os.get_terminal_size().columns)
                if len(self.dictionary) == 0:
                    print('No words in dictionary \"' + self.dictionary.name + '\".')
                else:
                    print(self.dictionary, end='')
                print('-' * os.get_terminal_size().columns)
                print('Done printing all definitions in dictionary \"' 
                      + self.dictionary.name + '\".\n')
            else:
                self.default('list ' + arg)

    def do_save(self, arg):
        if self.dict_exists():
            if self.file is None:
                shell_file_dir = os.path.dirname(__file__)
                shell_file_abs_pardir = os.path.abspath(os.path.join(shell_file_dir, os.pardir))
                _db_dir = os.path.join(shell_file_abs_pardir, 'db')
                
                while True:
                    db_dir = input(f'\nDefault directory is {_db_dir + os.sep}\nEnter directory path (skip to use default/"-" to quit save): ')
                    if db_dir.strip() == '':
                        db_dir = _db_dir
                    elif db_dir.strip() == '-':
                        print('No file being saved.')
                        break
                    if os.path.isdir(db_dir):
                        file_abs_path = f'{os.path.abspath(db_dir) + os.sep}{self.dictionary.name}.json'
                        print(f'Writing file "{file_abs_path}"\n')
                        self.file = open(file_abs_path, 'w')
                        json.dump(self.dictionary, self.file, cls=DictionaryEncoder, indent=2)
                        break
                    else:
                        print('Directory does not exist.')
            else:
                print()
                print(f'Rewriting file {self.file.name}. Backup of old file is {self.file.name.replace(".json", ".copy.json")}')
                print()
                shutil.copy2(self.file.name, self.file.name.replace(".json", ".copy.json"))
                json.dump(self.dictionary, self.file, cls=DictionaryEncoder, indent=2)

    def quit(self):
        if self.file is not None:
            self.file.close()

    def do_quit(self, arg):
        quit_confirm = input('Do you really want to exit (y/[n])? ')
        if quit_confirm == 'y':
            save_confirm = input('Do you want to save the progress so far ([y]/n)? ')
            if save_confirm == 'n':
                self.quit()
                return True
            else:
                pass

if __name__ == '__main__':
    Shell().cmdloop()