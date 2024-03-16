from WordRules import *

def test_letter_match():
    W = WordRules()
    assert W.letter_match(["s", "t", "r", "e", "e"], [0]) is True

test_letter_match()

