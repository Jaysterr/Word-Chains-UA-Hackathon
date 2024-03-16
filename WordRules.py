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
        self._prev_words = []
        try:
            # Open file of valid words
            file = open('words.txt')
        except FileNotFoundError:
            print('ERROR: File not found')
        else:
            # read the file and create list of valid words of specified length
            self._word_list = [word.strip().lower() for word in file if len(word.strip()) == SIZE and string.punctuation not in word]
            file.close()
    
    def contains_valid_word(self, letters: list[str], indexes: list[int]) -> bool:
        '''
        This method is used to determine if a user word (in the form of a list)
        is a valid guess by comparing it against the rules. It takes in a list
        of indexes which represent indexes where the letters shouldn't have changed
        based on the previous word. If the word is valid and new, it is added
        to the previous word list, and returns True, in any other case it returns
        False since a rule was violated.

        Parameters: letters is a list of strings representing a user word. 
        indexes is a list of integers representing indexes where letters should be 
        the same between the current user word and the previous word.

        Returns: True if the word is valid and False otherwise
        '''
        word = "".join(letters).lower() 
        if  word in self._word_list: # Valid word
            if word not in self._prev_words: # Previously guessed
                # Call all the rules we want
                if self.one_letter_match(word, indexes):
                    self._prev_words.append(word)
                    return True
        return False
    
    def check_word_len(self, letters: list[str]) -> bool:
        '''
        This function takes the letters input by the user and checks that they
        are a valid length. This function does not check if the word is valid.
        
        Parameters: letters is a list of strings which will all be single 
        characters. 

        Returns: True if the length is equal to the expected length and False 
        otherwise. 
        '''
        return len(letters) == self._SIZE

<<<<<<< Updated upstream
    def one_letter_match(self, word, indexes: list[int]) -> bool:
        ''' RULE: for optional game mode in which one letter must remain in the 
        same position and the word must be valid.'''
=======
    def one_letter_match(self, word, index) -> bool:
        ''' 
        This function provides a rule implementation and ensures that the rule 
        was followed. It is an optional game mode. 
        For this rule one letter must remain in the exact same position as it 
        was in the previous word. This position is determined randomly by the 
        game. 

        Parameters: word is a string representing the new word input by the user
            indexes is a list of integers that we will check for matches

        Returns: True if the rule is upheld and one letter remained in the same 
        position and False otherwise. '''
>>>>>>> Stashed changes
        prev_word = self._prev_words[-1]
        if prev_word[self._keep_index] == word[self._keep_index]:
            return True
        return False
    
    # Last matches new first or check multiple letters