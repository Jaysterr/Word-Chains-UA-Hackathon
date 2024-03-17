'''
File: GameManager.py
A manager for the game that handles all of the games logic. It interacts 
directly with the WordRules class and the GUI for the game. The logic of the game 
would run as follows:

1. toggle the gamemodes (toggle_gamemode())
2. determine the rules of the current game (run_game())
3. Get the current template the user must fill in (get_letters())
4. set the users word back into self._req_letters (set_user_word())
5. determine if the user's word is valid (is_valid())
6. Run the games and get a boolean value back. True means the game was successful
so continue onto the next game (GUI repeats this list from 2). False means the word
was repeated and so the game should end

@authors: Jakob Garcia and Caroline Schwengler
'''
import time
import random as rand
from WordRules import *


# TODO: Implement GameManager
class GameManager:

    def __init__(self) -> None:
        self._req_letters = ["", "", "", "", ""]  # list of letters that must be present in word (?)
        self._req_word_length = 5  # can be changed for potential gamemodes with longer/shorter words
        self._time = time.monotonic_ns() # keeping track of time (in ns to avoid floating point errors), init to current time
        self._word_rules = WordRules(self._req_word_length)
        self._gamemode = [True, False, False, False, False]
        self._indexes = []

    def set_user_word(self, word: list[str]) -> None:
        '''
        Setter method for the GUI to update the users word for this round of the
        game

        Parameters: A list of strings representing a word from the user
        '''
        for i in range(len(self._req_letters)):
            self._req_letters[i] = word[i]

    def get_letters(self) -> list[str]:
        '''
        A getter method for the GUI to use to determine what preset letters
        to display

        Returns: a list of string representing the preset template of strings
        determined by setting the rules.
        '''
        return self._req_letters

    def run_game(self):
        fixed_indexes = ["", "", "", "", ""] # Could get rid of and change all to self._req_letters
        # If we want this to work for other word lengths the line above should be tweaked all else works I think
        valid = [0, 1, 2, 3, 4]

        if self._gamemode[1]: # fist_last match enabled
            fixed_indexes[0] = WordRules.get_prev_word()[-1]
            valid.pop(0)

        if self._gamemode[4]: # multi letter match enabled
            amount = rand.randint(2, 4)
            i = 0
            while i < amount:
                found = valid.pop(rand.randint(0, len(valid)-1))
                if self._gamemode[3]:  # no dup
                    if WordRules.get_prev_word()[found] in fixed_indexes: # Would cause auto loss
                        valid.append(found)
                        continue
                fixed_indexes[found] = WordRules.get_prev_word()[found]
                if WordRules.determine_if_possible(fixed_indexes):
                    i += 1
                else: # no possible words we need new index
                    fixed_indexes[found] = ""
                    valid.append(found) # purposely do not increment loop 
                    valid.sort()
            
        if self._gamemode[0] and not self._gamemode[4]: # letter match enabled
            # Ensures letter match will not run if multi letter match is enabled
            placed = False
            while not placed:
                found = valid.pop(rand.randint(0, len(valid)-1))
                if self._gamemode[3] and WordRules.determine_if_possible(fixed_indexes): # no duplicate letters and valid
                    if WordRules.get_prev_word()[found] not in fixed_indexes: # Would cause auto loss
                        fixed_indexes[found] = WordRules.get_prev_word()[found]
                        placed = True
                elif WordRules.determine_if_possible(fixed_indexes): # check valid here this will need to change with Jakobs
                    fixed_indexes[found] = WordRules.get_prev_word()[found]
                    placed = True
                else:
                    valid.append(found) # purposely do not increment loop
                    valid.sort()

        if self._gamemode[2]: 
            letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
            index = rand.randint(0, len(valid)-1)
            while index not in valid: # Valid should never be empty at this point
                index = rand.randint(0, len(valid)-1)
            ###
            ### Super not done
            if self._gamemode[3] and WordRules.determine_if_possible(fixed_indexes): # no duplicate letters and valid
                pass
            ###
            while letter in fixed_indexes: # 
                letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
            #
            # Check collisions with duplicate letter
            #
            fixed_indexes[index] = letter

        # all are checked and done need to return which indexes are fixed (could instead of true false fix with letter here too and check =="")

    def toggle_gamemode(self, control: int) -> None:
        '''
        Setter method for GUI to update the control variables that determine
        which game rules should be active 
        '''
        self._gamemode[control] = not self._gamemode[control]

    
    def game_letter_match(self) -> bool:
        index = rand.randint(0, self._req_word_length-1)
        
        if self._word_rules.letter_match(self._req_letters, [index]):
            return True
        return False
        
    def game_first_last_match(self) -> bool:        
        if self._word_rules.first_last_match(self._req_letters):
            return True
        return False
        
    def game_random_letter_match(self) -> bool:
        index = rand.randint(0, self._req_word_length-1)
        letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
        
        if self._word_rules.random_letter_match(self._req_letters, (index, letter)):
            return True
        return False
        
    def game_no_duplicate_letters(self) -> bool:        
        if self._word_rules.no_duplicate_letters(self._req_letters):
            return True
        return False
    
    def game_multi_letter_match(self) -> bool:
        amount = rand.randint(2, 4)
        indexes = [0,1,2,3,4]
        for i in range(amount):
            indexes.pop(rand.randint(0, len(indexes)-1))
        
        if self._word_rules.letter_match(self._req_letters, [indexes]):
            return True
        return False
        
    def is_valid(self) -> bool:
        '''
        Determine if the user's word is valid based on the length and content.

        Returns: True if valid and False otherwise
        '''
        return self._word_rules.check_word_len() and self._word_rules.contains_valid_word()


    def get_time_elapsed(self) -> int:
        '''
        Returns the current time on the timer
        '''
        return time.monotonic_ns() - self._time # count up timer
        # return (10**10) - (time.monotonic_ns() - self._time) # alt countdown timer

    def reset_time(self) -> None:
        '''
        Resets the timer 
        '''
        self._time = time.monotonic_ns()
