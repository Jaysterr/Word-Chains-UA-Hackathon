'''
File: gamemanager.py
A manager for the game that handles all of the games logic. It interacts 
directly with the WordRules class and the GUI for the game. The flow of the game 
would run as follows:

1. toggle the gamemodes (toggle_gamemode())
2. gui calls run_game(), gamemanager calls corresponding methods in word_rules, which handles most of the logic,
wordrules returns a RoundResult enum, which is then passed to the GUI so everything can update accordingly.
3. repeat 2. until game over
4. reset_game() is called.

@authors: Jakob Garcia, Caroline Schwengler, Jesse Oved, Soren Abrams
Primary authors: Jakob Garcia, Caroline Schwengler
'''
import time
import random as rand
from wordrules import *
from roundresult import RoundResult
import json

# TODO: Implement GameManager
class GameManager:


    def __init__(self) -> None:
        self._user_input = ["", "", "", "", ""]
        self._req_letters = ["", "", "", "", ""]  # list of letters that must be present in word (?)
        self._req_word_length = 5  # can be changed for potential gamemodes with longer/shorter words
        self._time = None # keeping track of time (in ns to avoid floating point errors), init to None
        self._word_rules = WordRules(self._req_word_length)
        self._gamemode = [True, False, False, False, False] # First-Last match enabled by default
        self._time_limit = 10
        self._score = 0
        with open('data.json', 'r') as datafile: 
            self._persistent_data = json.loads(datafile.read())

    
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
            self.reset_game()
            return round_result
        
        if round_result is RoundResult.GOOD:
            self.increment_score()
            self.update_highscore()
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
        self._word_rules.toggle_active_rules(control)
        
        
    def get_time_elapsed(self) -> int:
        '''
        Returns the current time on the timer
        '''
        if self._time == None:
            return self._time_limit * (10**9)
        elif (self._time_limit * (10**9)) - (time.monotonic_ns() - self._time) < 0:
            self.reset_game()
            return 0
        return (self._time_limit * (10**9)) - (time.monotonic_ns() - self._time) # countdown timer


    def set_time_limit(self, time_limit: int) -> None:
        self.time_limit = time_limit
        
    def reset_time(self) -> None:
        '''
        Resets the timer
        '''
        self._time = time.monotonic_ns()
        
    def reset_game(self) -> None: # reset and/or initialize the game
        '''
        Resets the game, if player got a highscore then it updates the _highest_score attribute
        '''
        self._time = None
        self._user_input = ["", "", "", "", ""]
        self._word_rules.reset_prev_words()
        self._word_rules.reset_req_letters()
        self._score = 0


    def update_highscore(self):
        '''
        updates highscore and caches it. You better not be manually editing the data.json file :(
        '''
        if (self._persistent_data['highscore'] < self._score):
            self._persistent_data['highscore'] = self._score
            with open('data.json', 'w') as datafile:
                datafile.write(json.dumps(self._persistent_data))


    def increment_score(self):
        score_increment = 0
        rules = self._word_rules._active_rules
        if rules[0] == True:
            score_increment += 1
        elif rules[1] == True:
            score_increment += 1
        if rules[2] == True:
            score_increment += 1
        if rules[3] == True:
            score_increment += 1
        if rules[4] == True:
            score_increment += 1
        self._score += score_increment

    def get_score(self):
        return self._score
    
    def get_highscore(self):
        
        return self._persistent_data['highscore']
    
    def get_req_letters(self):
        return self._word_rules.get_req_letters()
    
    def get_time_limit(self):
        return self._time_limit