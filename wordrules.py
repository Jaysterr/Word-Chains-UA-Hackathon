'''
File: wordrules.py
defines all the possible rules/restrictions for a word and different game modes.
It is capable of checking if a word is valid and running 5 different games. 
There is the base game of letter match (base and random version handled more by 
the game manager), a first letter matching last letter game,a random letter matching 
game, and a no letter duplicates matching game.

@authors: Jakob Garcia, Caroline Schwengler, Jesse Oved
'''
import string
from roundresult import RoundResult
import random as rand

class WordRules:
    
    def __init__(self, SIZE: int=5) -> None:
        '''
        Initialize the WordRules object. Creates attributes for the constant
        size of the words which can vary depending on the game mode. It also
        creates an attribute for the list of valid words read in from a text
        file. An attribute is also kept for the last 

        Parameters: SIZE is a int constant representing the specified word 
        size of the game. It defaults to 5 if no constant is given.
        '''
        self._active_rules = [True, False, False, False, False] # Single Letter Match enabled by default
        self._req_letters = ["", "", "", "", ""] # list of letters that must be present in word]
        self._SIZE = SIZE
        self._prev_words = [] # list of lists, each sublist representing the characters of a word
        try:
            # Open file of valid words
            file = open('words.txt')
        except FileNotFoundError:
            print('ERROR: File not found')
        else:
            # read the file and create list of valid words of specified length
            self._word_list = [word.strip().lower() for word in file if len(word.strip()) == SIZE and string.punctuation not in word]
            file.close()
        
    def toggle_active_rules(self, index: int):
        self._active_rules[index] = not self._active_rules[index]
        
    def is_not_duplicate_word(self, letters: list[str]) -> bool: 
        '''
        This method is used to determine if a user word (in the form of a list)
        is a valid guess by comparing it against the rules. If the word is a new
        word, it returns True

        Parameters: letters is a list of strings representing a user word. 

        Returns: True if the word is valid and False otherwise
        '''
        # word = "".join(letters).lower()
        if letters not in self._prev_words: # Previously guessed
            return True
        return False
    
    def contains_valid_word(self, letters: list[str]) -> bool: 
        '''
        This method is used to determine if a user word (in the form of a list)
        is a valid guess by comparing it against the rules. If the word is a valid
        word in the word list, it returns True

        Parameters: letters is a list of strings representing a user word. 

        Returns: True if the word is valid and False otherwise
        '''
        word = "".join(letters).lower() 
        if word in self._word_list: # Valid word
            return True
        return False


    def get_prev_word(self) -> str:
        '''
        Return whatever the previous word was
        '''
        return self._prev_words[-1]

    
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
    

    def determine_if_possible(self, letters: list[str]) -> bool:
        '''
        This method is used for determining if a given layout of characters
        has any possible words that can be created by filling in the blanks. After
        determining if words are possible, it checks how many of those words have 
        already been guessed. If there are no possible words after checking 
        for previous guesses, the method returns False. It returns True if there
        is at least one possible word to guess.

        Parameters: Letters is a list of strings that represents a layout the
        user will guess in.

        Returns: True if there is a possible word and False otherwise
        '''
        possible_words = []
        first_run = True
        # iterate through the users word
        for i in range(len(letters)):
            if letters[i] != '':
                # if we have not found possible words based on the leading char yet, 
                # determine possible words
                if possible_words == [] and first_run:
                    for word in self._word_list:
                        if word[i] == letters[i]:
                            possible_words.append(word)
                elif possible_words == []:
                    return False
                else:
                    # If we do have possible words, filter out the words that don't match the other characters
                    j = 0
                    new_words = []
                    while j < len(possible_words): 
                        if possible_words[j][i] != letters[i]:
                            possible_words.pop(j)
                            j-=1
                        else:
                            new_words.append(possible_words[j])

                        j += 1
                    #if new_words != []:
                    #    possible_words = new_words
            first_run = False
        #print(possible_words)
        # Account for words already used, and determine if there are still possible words
        return len(set(possible_words) - set(["".join(x) for x in self._prev_words])) != 0
    
    
    def matches_letters(self, letters: list[str]) -> bool:
        '''
        generic method that checks if the items of 'letters' match the non-empty items of 'req_letters'
        Should only be run AFTER all other validation checks, including checking for duplicate letters
        '''
        for i in (range(len(letters))):
            if self._req_letters[i] == "":
                continue
            elif letters[i] != self._req_letters[i]:
                return False
        self._prev_words.append(letters)
        return True
    
    
    def check_word(self, input: str) -> RoundResult:
        '''
        checks whether the given word is valid and follows all of the rules.
        :return: a RoundResult enum
        '''
        is_valid = self.check_validity(input)
        
        if not is_valid[1]:
            # Word was a repeat of a previous word
            return RoundResult.REPEAT

        if not is_valid[0]: 
            # word was not duplicate, but was invalid
            return RoundResult.INVALID
        
        if self._active_rules[4]:
            my_set = set(input)
            if my_set.len() != 5:
                return RoundResult.INVALID
        
        won_round = self.matches_letters(input)
        
        if (won_round):
            return RoundResult.GOOD
        else:
            return RoundResult.INVALID

    def check_validity(self, input: str) -> bool:
        '''
        checks the word in input
        :return: a tuple formatted as:
                    (is_valid(), is_repeat())
                    (True, True) = accepted word
                    (False, True) = invalid word
                    (True, False) = repeat word
                    (False, False) = repeat invalid word
        '''
        return (self.check_word_len(input) and self.contains_valid_word(input), \
                self.is_not_duplicate_word(input))
    
    
    def determine_rules(self):
        # This method should only be run AFTER the user inputs their first word. And then every round after that
        
        # Pretty sure these are the current indexes of game rules
        # single letter match - 0 
        # multi letter match - 1 
        # first last - 2 
        # random letter - 3 
        # no duplicates - 4

        valid = [0, 1, 2, 3, 4]
        future_letters = ["", "", "", "", ""]
        
        # FIRST-LAST MATCH
        # This is run first to ensure it gets the first position, and can pop that position in 'valid'
        if self._active_rules[2]:
            future_letters = [self.get_prev_word()[-1], "", "", "", ""]
            valid.pop(0)
        
        # MULTI-LETTER MATCH
        if self._active_rules[1]: # multi letter match enabled
            # This works on its own, need to test with others, does not account for if rule[4] enabled
            if self._active_rules[3]:
                amt_to_match = rand.randint(1, 2)
            else:
                amt_to_match = rand.randint(1, 3)
            possible_i = [i for i in valid]
            keep_i = possible_i.pop(rand.randint(0, len(possible_i) - 1))
            future_letters[keep_i] = self.get_prev_word()[keep_i]
            amt_to_match -= 1
            
            while amt_to_match != 0:
                keep_i = possible_i.pop(rand.randint(0, len(possible_i) - 1))
                future_letters[keep_i] = self.get_prev_word()[keep_i]
                amt_to_match -= 1
                if not self.determine_if_possible(future_letters):
                    future_letters[keep_i] = ""
                    possible_i.append(keep_i)
                    amt_to_match += 1
            valid = possible_i
                
        # SINGLE LETTER MATCH
        # elif ensures this is only run if multi letter match was not enabled
        elif self._active_rules[0] and not self._active_rules[1]: # letter match enabled
            placed = False
            while not placed:
                found = valid.pop(rand.randint(0, len(valid)-1))
                if self._gamemode[4]: # no duplicate letters and valid
                    if self._word_rules.get_prev_word()[found] in future_letters: # Would cause auto loss
                        valid.append(found)
                        continue   # Move to next iteration of loop to generate different letter        
                future_letters[found] = self.get_prev_word()[found]
                if self.determine_if_possible(future_letters): 
                    placed = True # Break out of loop
                else:
                    future_letters[found] = ""
                    valid.append(found) # purposely do not increment loop

        # RANDOM LETTER MATCH
        if self._active_rules[3]: 
            # Working but is not yet accounting for is rule[4] is enabled
            good = False
            while not good:
                index = rand.randint(0, len(valid)-1)
                while index not in valid: # Valid should never be empty at this point
                    index = rand.randint(0, len(valid)-1) # Will get valid index
                letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
                if self._active_rules[4]: # no duplicate letters and valid
                    while letter in future_letters: 
                        letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
                future_letters[index] = letter
                if not self.determine_if_possible(future_letters):
                    future_letters[index] = ""
                else:
                    valid.remove(index)
                    good = True
    
        self._req_letters = future_letters
    
    
    def reset_prev_words(self):
        '''
        For restarting the game. Resets the self._prev_words list
        '''
        self._prev_words = []
        
    def reset_req_letters(self):
        '''
        For restarting the game. Resets the self._req_letters list
        '''
        self._req_letters = ["", "", "", "", ""]
        
    def get_req_letters(self):
        return self._req_letters
