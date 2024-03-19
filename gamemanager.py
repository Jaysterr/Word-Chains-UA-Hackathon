'''
File: gamemanager.py
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

@authors: Jakob Garcia, Caroline Schwengler, Jesse Oved
'''
import time
import random as rand
from wordrules import *
from roundresult import RoundResult

# TODO: Implement GameManager
class GameManager:

    def __init__(self) -> None:
        self._user_input = ["", "", "", "", ""]
        self._req_letters = ["", "", "", "", ""]  # list of letters that must be present in word (?)
        self._req_word_length = 5  # can be changed for potential gamemodes with longer/shorter words
        self._time = None # keeping track of time (in ns to avoid floating point errors), init to None
        self._word_rules = WordRules(self._req_word_length)
        self._gamemode = [True, False, False, False, False] # First-Last match enabled by default
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
        return self._word_rules.get_req_letters()

    def run_game(self, user_input: str) -> RoundResult:
        '''
        To be used by the GUI in order to run a game based on whatever rules are 
        set in self._gamemode.

        Returns: True if all specified games run successfully and False otherwise
        '''
        
        # check if word is valid
        round_result = self._word_rules.check_word(user_input)
        
        if round_result is RoundResult.REPEAT:
            # Word was duplicate, end game
            # TODO
            self.reset_game()
            return round_result
        
        if round_result is RoundResult.GOOD:
            self.add_score(1)
            self.reset_time()
            self._word_rules.determine_rules()
            return round_result
        else:
            return round_result
            


    def toggle_gamemode(self, control: int) -> None:
        '''
        Setter method for GUI to update the control variables that determine
        which game rules should be active 
        '''
        print("auigebew")
        self._word_rules.toggle_active_rules(control)
        
    def is_valid(self) -> bool:
        '''
        Determine if the user's word is valid based on the length, and content

        Returns: True if valid and False otherwise
        '''
        return self._word_rules.check_word_len(self._user_input) and \
               self._word_rules.contains_valid_word(self._user_input) and ((not self._gamemode[4]) or self._word_rules.no_duplicate_letters(self._user_input))

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
        return (self.is_valid(), self._word_rules.is_not_duplicate_word(self._user_input))

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
        self._user_input = ["", "", "", "", ""]
        self._word_rules.reset_prev_words()
        self._word_rules.reset_req_letters()
        self._score = 0

    def add_score(self, amount: int):
        self._score += amount

    def get_score(self):
        return self._score
    
    def get_req_letters(self):
        return self._word_rules.get_req_letters()