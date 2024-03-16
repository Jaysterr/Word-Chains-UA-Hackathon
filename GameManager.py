# GameManager.py
# A manager for... the game :O
# handles game logic

import WordRules

# TODO: Implement GameManager
class GameManager:
    
    req_letters = ["", "", "", "", ""] # list of letters that must be present in word (?)
    req_word_length = 5 # can be changed for potential gamemodes with longer/shorter words
    
    def __init__(self) -> None:
        return
    
    def is_valid_word(self, word: str) -> bool:
        return False
    