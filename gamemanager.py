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

    def determine_rules(self):
        # This needs to be rerun each round of the game
        # If we want this to work for other word lengths the line above should be tweaked all else works I think
        valid = [0, 1, 2, 3, 4]

        if self._gamemode[1]: # fist_last match enabled
            self._req_letters[0] = self._word_rules.get_prev_word()[-1]
            valid.pop(0)

        if self._gamemode[4]: # multi letter match enabled
            amount = rand.randint(2, 4)
            i = 0
            while i < amount:
                found = valid.pop(rand.randint(0, len(valid)-1))
                if self._gamemode[3]:  # no dup
                    if self._word_rules.get_prev_word()[found] in self._req_letters: # Would cause auto loss
                        valid.append(found)
                        continue
                self._req_letters[found] = self._word_rules.get_prev_word()[found]
                if self._word_rules.determine_if_possible(self._req_letters):
                    i += 1
                else: # no possible words we need new index
                    self._req_letters[found] = ""
                    valid.append(found) # purposely do not increment loop 
                    valid.sort()
            
        if self._gamemode[0] and not self._gamemode[4]: # letter match enabled
            # Ensures letter match will not run if multi letter match is enabled
            placed = False
            while not placed:
                found = valid.pop(rand.randint(0, len(valid)-1))
                if self._gamemode[3]: # no duplicate letters and valid
                    if self._word_rules.get_prev_word()[found] in self._req_letters: # Would cause auto loss
                        valid.append(found)
                        continue                
                self._req_letters[found] = self._word_rules.get_prev_word()[found]
                if self._word_rules.determine_if_possible(self._req_letters): 
                    placed = True
                else:
                    self._req_letters[found] = ""
                    valid.append(found) # purposely do not increment loop
                    valid.sort()

        if self._gamemode[2]: 
            index = rand.randint(0, len(valid)-1)
            while index not in valid: # Valid should never be empty at this point
                index = rand.randint(0, len(valid)-1) # Will get valid index
            good = False
            while not good:
                letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
                if self._gamemode[3]: # no duplicate letters and valid
                    while letter in self._req_letters: 
                        letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
                self._req_letters[index] = letter
                if not self._word_rules.determine_if_possible(self._req_letters):
                    self._req_letters[found] = ""
                    valid.append(found) # purposely do not increment loop
                    valid.sort()
                else:
                    good = True

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
