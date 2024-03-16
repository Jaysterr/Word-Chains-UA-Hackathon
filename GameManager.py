# GameManager.py
# A manager for... the game :O
# handles game logic

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
        self._gamemode = [1, 0, 0, 0, 0]
        self._indexes = []

    def set_user_word(self, word: list[str]) -> None:
        for i in range(len(self._req_letters)):
            self._req_letters[i] = word[i]

    def run_game(self):
        if self._gamemode[1] == 1:
            return self.game_first_last_match()
        elif self._gamemode[2] == 1:
            return self.game_random_letter_match()
        elif self._gamemode[3] == 1:
            return self.game_no_duplicate_letters()
        elif self._gamemode[4] == 1:
            return self.game_multi_letter_match()
        else:
            return self.game_letter_match()

    def change_gamemode(self, controls: list[int]) -> None:
        self._gamemode = controls

    
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
        return self._word_rules.check_word_len()


    def get_time_elapsed(self):
        return time.monotonic_ns() - self._time # count up timer
        # return (10**10) - (time.monotonic_ns() - self._time) # alt countdown timer

    def reset_time(self):
        self._time = time.monotonic_ns()
