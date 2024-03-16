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
        '''
        Initialize the WordRules object. Creates attributes for the constant
        size of the words which can vary depending on the game mode. It also
        creates an attribute for the list of valid words read in from a text
        file. An attribute is also kept for the last 

        Parameters: SIZE is a int constant representing the specified word 
        size of the game. It defaults to 5 if no constant is given.
        '''
        self._SIZE = SIZE
        try:
            file = open('words.txt')
        except FileNotFoundError:
            print('ERROR: File not found')
        else:
            self._word_list = [word.strip().lower() for word in file if len(word.strip()) == SIZE and string.punctuation not in word]
            file.close()
    
    def contains_valid_word(self, letters: list[str]) -> bool:
        return "".join(letters).lower() in self._word_list
    
    def check_word_len(self, letters: list[str]) -> bool:
        return len(letters) == self._SIZE
