'''
File: GameManager.py
A manager for the game that handles all of the games logic. It interacts 
directly with the WordRules class and the GUI for the game. The logic of the game 
would run as follows:

1. toggle the gamemodes (toggle_gamemode())
2. determine the rules of the current game (determine_rules())
    - this sets self._req_letters to the required letters for this round
3. Get the current template the user must fill in (get_letters())
4. set the users word into self._user_input (set_user_word())
5. determine if the user's word is valid (is_valid())
6. Run the games and get a boolean value back. True means the game was successful
so continue onto the next game (GUI repeats this list from 2). False means the word
was repeated and so the game should end (run_game())
7. If the game is reset, call the reset game method (reset_game()).

toggle gamemodes
get required word from game
input user word
run game

@authors: Jakob Garcia and Caroline Schwengler
'''
import time
import random as rand
from WordRules import *


# TODO: Implement GameManager
class GameManager:

    def __init__(self) -> None:
        self._user_input = ["", "", "", "", ""]
        self._req_letters = ["", "", "", "", ""]  # list of letters that must be present in word (?)
        self._req_word_length = 5  # can be changed for potential gamemodes with longer/shorter words
        self._time = None # keeping track of time (in ns to avoid floating point errors), init to None
        self._word_rules = WordRules(self._req_word_length)
        self._gamemode = [False, False, True, False, False] # First-Last match enabled by default
        self._time_limit = 15
        self._score = 0

    
    def set_user_word(self, word: list[str]) -> None:
        '''
        Setter method for the GUI to update the users word for this round of the
        game

        Parameters: A list of strings representing a word from the user
        '''
        self._user_input = word
        # for i in range(len(self._req_letters)):
        #     self._req_letters[i] = word[i]

    def get_letters(self) -> list[str]:
        '''
        A getter method for the GUI to use to determine what preset letters
        to display

        Returns: a list of string representing the preset template of strings
        determined by setting the rules.
        '''
        return self._req_letters

    def determine_rules(self):
        # This needs to be rerun each round of the game
        # If we want this to work for other word lengths the line above should be tweaked 
        valid = [0, 1, 2, 3, 4]
        future_letters = ["", "", "", "", ""]

        # SINGLE LETTER MATCH
        if self._gamemode[0] and not self._gamemode[1]: # letter match enabled
            # Ensures letter match will not run if multi letter match is enabled
            placed = False
            while not placed:
                found = valid.pop(rand.randint(0, len(valid)-1))
                if self._gamemode[3]: # no duplicate letters and valid
                    if self._word_rules.get_prev_word()[found] in future_letters: # Would cause auto loss
                        valid.append(found)
                        continue                
                future_letters[found] = self._word_rules.get_prev_word()[found]
                if self._word_rules.determine_if_possible(future_letters): 
                    placed = True
                else:
                    future_letters[found] = ""
                    valid.append(found) # purposely do not increment loop
                    valid.sort()
        
        # MULTI-LETTER MATCH
        # if self._gamemode[1]: # multi letter match enabled
        #     possible_i = [i for i in valid]
        #     print(possible_i)
        #     keep_i = possible_i.pop(rand.randint(0, len(possible_i) - 1))
        #     future_letters[keep_i] = self._user_input[keep_i]
        #     while (not self._word_rules.determine_if_possible(
        #             future_letters)) and len(possible_i) != 0:
        #         print("sadu")
        #         print(future_letters)
        #         future_letters[keep_i] = ""
        #         keep_i = possible_i.pop(
        #             rand.randint(0, len(possible_i) - 1))
        #         future_letters[keep_i] = self._user_input[keep_i]
        #     if len(possible_i) == 0:
        #         future_letters[keep_i] = ""
                
        # FIRST-LAST MATCH
        if self._gamemode[2]: # first_last match enabled
            future_letters = [self._user_input[-1], "", "", "", ""]
            # future_letters = [self._req_letters[4], "", "", "", ""]
            # valid.pop(0)
        
        # RANDOM LETTER MATCH
        # if self._gamemode[3]: 
        #     index = rand.randint(0, len(valid)-1)
        #     while index not in valid: # Valid should never be empty at this point
        #         index = rand.randint(0, len(valid)-1) # Will get valid index
        #     good = False
        #     while not good:
        #         letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
        #         if self._gamemode[3]: # no duplicate letters and valid
        #             while letter in self._req_letters: 
        #                 letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
        #         self._req_letters[index] = letter
        #         if not self._word_rules.determine_if_possible(self._req_letters):
        #             self._req_letters[found] = ""
        #             valid.append(found) # purposely do not increment loop
        #             valid.sort()
        #         else:
        #             good = True
    
        # if self._gamemode[3]: # random letter
        #     index = rand.randint(0, len(valid)-1)
        #     letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
        #     self._req_letters[index] = letter
        #     valid.pop(index)




        self._req_letters = future_letters

    def run_game(self) -> bool:
        '''
        To be used by the GUI in order to run a game based on whatever rules are 
        set in self._gamemode.

        Returns: True if all specified games run successfully and False otherwise
        '''
        # First check if word is valid
        validity = self.check_word()
        if not validity[1]:
            # Word was duplicate, end game
            self.reset_game()
            return False

        if not validity[0]: 
            # word was not duplicate, but was invalid, so return false
            return False
        
        results = True

        results = results and self._word_rules.matches_letters(self._user_input, self._req_letters)
        # future_letters = ["", "", "", "", ""]
        # SINGLE LETTER MATCH
        if self._gamemode[0]:
            results = results and self._word_rules.matches_letters(self._user_input, self._req_letters)
        # MULTI-LETTER MATCH
        # if self._gamemode[1]:
        #     results = results and self._word_rules.random_letter_match(self._req_letters, [0,1,2,3,4])
        # FIRST-LAST LETTER MATCH
        if self._gamemode[2]:
            results = results and self._word_rules.matches_letters(self._user_input, self._req_letters)
            #future_letters = [self._req_letters[4], "", "", "", ""]
        # RANDOM LETTER MATCH
        # if self._gamemode[3]:
        #     results = results and self._word_rules.no_duplicate_letters(self._req_letters, [0,1,2,3,4])
        # if self._gamemode[4]:
        #     results = results and self._word_rules.letter_match(self._req_letters, [0,1,2,3,4])
        #     """ possible_i = [i for i in range(int(self._gamemode[1]), 5)]
        #     keep_i = possible_i.pop(rand.randint(0, len(possible_i) - 1))
        #     future_letters[keep_i] = self._req_letters[keep_i]
        #     while (not self._word_rules.determine_if_possible(future_letters)) and len(possible_i) != 0:
        #         print("sadu")
        #         print(future_letters)
        #         future_letters[keep_i] = ""
        #         keep_i = possible_i.pop(rand.randint(0, len(possible_i) - 1))
        #         future_letters[keep_i] = self._req_letters[keep_i]
        #     if len(possible_i) == 0:
        #         future_letters[keep_i] = ""
        # self._req_letters = future_letter """
        
        if results == True:
            self.add_score(1)
            self.reset_time()
            self.determine_rules()

        return results

    def toggle_gamemode(self, control: int) -> None:
        '''
        Setter method for GUI to update the control variables that determine
        which game rules should be active 
        '''
        print("auigebew")
        # self._word_rules.toggle_active_rules(control)
        self._gamemode[control] = not self._gamemode[control]
        
    def is_valid(self) -> bool:
        '''
        Determine if the user's word is valid based on the length, and content

        Returns: True if valid and False otherwise
        '''
        return self._word_rules.check_word_len(self._user_input) and \
               self._word_rules.contains_valid_word(self._user_input)

    def get_time_elapsed(self) -> int:
        '''
        Returns the current time on the timer
        '''
        #return time.monotonic_ns() - self._time # count up timer
        if self._time == None:
            return self._time_limit * (10**9)
        elif (self._time_limit * (10**9)) - (time.monotonic_ns() - self._time) < 0:
            return 0
        return (self._time_limit * (10**9)) - (time.monotonic_ns() - self._time) # alt countdown timer

    def check_word(self):
        '''
        checks the word currently in self._req_letters
        :return: a tuple formatted as:
                    (is_valid(), is_repeat())
                    (True, True) = accepted word
                    (False, True) = invalid word
                    (True, False) = repeat word
                    (False, False) = repeat invalid word
        '''
        return (self.is_valid(), self._word_rules.is_not_duplicate_word(self._req_letters))

    def set_time_limit(self, time_limit: int) -> None:
        self.time_limit = time_limit
        
    def reset_time(self) -> None:
        '''
        Resets the timer
        '''
        self._time = time.monotonic_ns()
        
    def reset_game(self) -> None: # reset and/or initialize the game
        '''
        Resets the game
        '''
        self._time = None
        self._req_letters = ["", "", "", "", ""]
        # self._gamemode = [False, True, False, False, False]
        self.determine_rules()
        self._word_rules.reset_prev_words()
        self._score = 0

    def add_score(self, amount: int):
        self._score += amount
