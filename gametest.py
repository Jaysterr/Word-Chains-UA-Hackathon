from WordRules import *

def test_letter_match():
    W = WordRules()
    assert W.letter_match(["s", "t", "r", "e", "e"], [0]) is True
    assert W.letter_match(["s", "t", "t", "e", "e"], [0]) is True
    print(W.letter_match(["9", "t", "r", "e", "e"], [0]))
    assert W.letter_match(["9", "t", "r", "e", "e"], [0]) is False
    # assert W.letter_match(["c", "a", "k", "e", "s"], [0]) is False

test_letter_match()

