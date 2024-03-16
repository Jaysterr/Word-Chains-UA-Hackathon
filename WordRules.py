# WordRules
# defines all the possible rules/restrictions for a word

#    not sure exactly how this should be structured/operated yet. 
#    But seems like it may be a good idea to seperate rules to their own file
#    so we can more easily add additional rules and such, and keep things readable
#
#    could be merged with GameManager if it turns out there isnt good enough reason to seperate

# TODO: Implement WordRules
import string
import random

class WordRules:
    def __init__(self, SIZE: int=5):
        self._SIZE = SIZE
        self._prev_words = []
        try:
            file = open('words.txt')
        except FileNotFoundError:
            print('ERROR: File not found')
        else:
            self._word_list = [word.strip().lower() for word in file if len(word.strip()) == SIZE and string.punctuation not in word]
            file.close()
    
    def contains_valid_word(self, letters: list[str], index) -> bool:
        word = "".join(letters).lower() 
        if  word in self._word_list: # Valid word
            if word not in self._prev_words: # Previously guessed
                self._prev_words.append(word)
                # Call all the rules we want
                if self.one_letter_match(word, index):
                    return True
        return False
    
    def check_word_len(self, letters: list[str]) -> bool:
        return len(letters) == self._SIZE

    def one_letter_match(self, word, index) -> bool:
        ''' RULE: for optional game mode in which one letter must remain in the 
        same position and the word must be valid.'''
        prev_word = self._prev_words[-1]
        if prev_word[self._keep_index] == word[self._keep_index]:
            return True
        return False
    
    # Last matches new first or check multiple letters