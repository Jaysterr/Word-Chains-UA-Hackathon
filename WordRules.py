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

    def letter_match(self, letters: list[str], indexes: list[int]) -> bool:
        ''' 
        This function provides a rule implementation and ensures that the rule 
        was followed. It is an optional game mode. 
        For this rule a specified number of letters must remain in the exact 
        same position as it was in the previous word. These positions are determined
        randomly by the game. 

        Parameters: letters is a list of strings representing the new word inputted by the user
        indexes is a list of integers that we will check for matches

        Returns: True if the rule is upheld and the specified letters remained in the same 
        position and False otherwise. 
        '''
        prev_word = self._prev_words[-1]

        for index in indexes:
            # Compare previous word to current word 
            if prev_word[index] != letters[index]:
                return False
        return True
    
    def first_last_match(self, letters: list[str]) -> bool:
        '''
        This function provides a rule implementation and ensures that the rule 
        was followed. It is an optional game mode. 
        For this rule the last letter of the previous word must match the first
        letter of the new word.

        Parameters: letters is a list of strings representing the new word inputted by the user

        Returns: True if the rule is upheld and False otherwise. 
        '''
        prev_word = self._prev_words[-1]

        if prev_word[-1] == letters[0]:
                return True
        return False


