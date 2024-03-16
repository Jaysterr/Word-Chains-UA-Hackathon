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

    def determine_gamemode(self, controls: list[int]) -> None:
        self._gamemode = controls

    
    def game_letter_match(self):
        index = rand.randint(0, self._req_word_length-1)
        
        self._word_rules.letter_match(self._req_letters)


    
    def is_valid_word(self, word: list[str]) -> bool:
        return False

    def get_time_elapsed(self):
        return time.monotonic_ns() - self._time # count up timer
        # return (10**10) - (time.monotonic_ns() - self._time) # alt countdown timer

    def reset_time(self):
        self._time = time.monotonic_ns()
