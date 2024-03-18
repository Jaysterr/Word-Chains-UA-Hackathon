'''
File: GameManager.py
A manager for the game that handles all of the games logic. It interacts 
directly with the WordRules class and the GUI for the game. The logic of the game 
would run as follows:

1. toggle the gamemodes (toggle_gamemode())
2. determine the rules of the current game (determine_rules())
3. Get the current template the user must fill in (get_letters())
4. set the users word back into self._req_letters (set_user_word())
5. determine if the user's word is valid (is_valid())
6. Run the games and get a boolean value back. True means the game was successful
so continue onto the next game (GUI repeats this list from 2). False means the word
was repeated and so the game should end (run_game())
7. If the game is reset, call the reset game method (reset_game()).

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
        self._time = None # keeping track of time (in ns to avoid floating point errors), init to None
        self._word_rules = WordRules(self._req_word_length)
        self._gamemode = [True, False, False, False, False]
        self._time_limit = 15
        self._score = 0

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
        future_letters = ["", "", "", "", ""]
        if self._word_rules.check_first_round(): # first round only random letter has rule in effect
            if self._gamemode[2]: # random letter
                index = rand.randint(0, len(valid)-1)
                letter = rand.choice("abcdefghijklmnopqrstuvwxyz")
                self._req_letters[index] = letter
                valid.pop(index)
        else:
            if self._gamemode[1]: # first_last match enabled
                future_letters = [self._req_letters[4], "", "", "", ""]
                valid.pop(0)
            if self._gamemode[4]: # multi letter match enabled
                possible_i = [i for i in valid]
                print(possible_i)
                keep_i = possible_i.pop(rand.randint(0, len(possible_i) - 1))
                future_letters[keep_i] = self._req_letters[keep_i]
                while (not self._word_rules.determine_if_possible(
                        future_letters)) and len(possible_i) != 0:
                    print("sadu")
                    print(future_letters)
                    future_letters[keep_i] = ""
                    keep_i = possible_i.pop(
                        rand.randint(0, len(possible_i) - 1))
                    future_letters[keep_i] = self._req_letters[keep_i]
                if len(possible_i) == 0:
                    future_letters[keep_i] = ""
                
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
            self._req_letters = future_letters

    def run_game(self) -> bool:
        '''
        To be used by the GUI in order to run a game based on whatever rules are 
        set in self._gamemode.

        Returns: True if all specified games run successfully and False otherwise
        '''
        results = True
        #future_letters = ["", "", "", "", ""]
        if self._gamemode[0]:
            results = results and self._word_rules.letter_match(self._req_letters, [0,1,2,3,4])
        if self._gamemode[1]:
            results = results and self._word_rules.first_last_match(self._req_letters)
            #future_letters = [self._req_letters[4], "", "", "", ""]
        if self._gamemode[2]:
            results = results and self._word_rules.random_letter_match(self._req_letters, [0,1,2,3,4])
        if self._gamemode[3]:
            results = results and self._word_rules.no_duplicate_letters(self._req_letters, [0,1,2,3,4])
        if self._gamemode[4]:
            results = results and self._word_rules.letter_match(self._req_letters, [0,1,2,3,4])
            """ possible_i = [i for i in range(int(self._gamemode[1]), 5)]
            keep_i = possible_i.pop(rand.randint(0, len(possible_i) - 1))
            future_letters[keep_i] = self._req_letters[keep_i]
            while (not self._word_rules.determine_if_possible(future_letters)) and len(possible_i) != 0:
                print("sadu")
                print(future_letters)
                future_letters[keep_i] = ""
                keep_i = possible_i.pop(rand.randint(0, len(possible_i) - 1))
                future_letters[keep_i] = self._req_letters[keep_i]
            if len(possible_i) == 0:
                future_letters[keep_i] = ""
        self._req_letters = future_letter """
        return results

    def toggle_gamemode(self, control: int) -> None:
        '''
        Setter method for GUI to update the control variables that determine
        which game rules should be active 
        '''
        print("auigebew")
        self._gamemode[control] = not self._gamemode[control]
        
    def is_valid(self) -> bool:
        '''
        Determine if the user's word is valid based on the length and content.

        Returns: True if valid and False otherwise
        '''
        return self._word_rules.check_word_len(self._req_letters) and self._word_rules.contains_valid_word(self._req_letters)

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

    def check_word(self) -> (bool, bool):
        '''
        checks the word currently in self._req_letters
        :return: a tuple formatted as:
                    (is_valid(), is_repeat())
                    (True, False) = accepted word
                    (False, False) = invalid word
                    (True, True) = repeat word
                    (False, True) = repeat invalid word
        '''
        return (self.is_valid(), not self._word_rules.contains_duplicate_word(self._req_letters))

    def set_time_limit(self, time_limit: int) -> None:
        self.time_limit = time_limit
        
    def reset_time(self) -> None:
        '''
        Resets the timer
        '''
        self._time = time.monotonic_ns()
        
    def reset_game(self) -> None:
        '''
        Resets the game
        '''
        self.reset_time()
        self._req_letters = ["", "", "", "", ""]
        self._gamemode = [True, False, False, False, False]
        self._word_rules.reset_prev_words()
        self._score = 0

    def add_score(self, amount: int):
        self._score += amount
