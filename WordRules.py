# WordRules
# defines all the possible rules/restrictions for a word

#    not sure exactly how this should be structured/operated yet. 
#    But seems like it may be a good idea to seperate rules to their own file
#    so we can more easily add additional rules and such, and keep things readable
#
#    could be merged with GameManager if it turns out there isnt good enough reason to seperate

# TODO: Implement WordRules
import string
class WordRules:
    def __init__(self, SIZE: int=5):
        try:
            file = open('words.txt')
        except FileNotFoundError:
            print('ERROR: File not found')
        else:
            self._word_list = [word.strip().lower() for word in file if len(word.strip()) == SIZE and string.punctuation not in word]
            file.close()
    
    def contains_letters(self, letters: list[str]) -> bool:
        return "".join(letters).lower() in self._word_list
    
    def check_word_len(self, letters: list[str], SIZE: int=5) -> bool:
        return len(letters) == SIZE
