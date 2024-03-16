from WordRules import *

def test_valid_words_letter_match():
    W = WordRules()
    assert W.letter_match(["s", "t", "r", "e", "e"], [0]) is False
    assert W.letter_match(["9", "t", "r", "e", "e"], [0]) is False

    assert W.letter_match(["c", "a", "k", "e", "s"], [0]) is True

    # no duplicates
    assert W.letter_match(["c", "a", "k", "e", "s"], [0]) is False
    assert W.letter_match(["c", "a", "k", "e", "s"], [1]) is False
    assert W.letter_match(["c", "a", "k", "e", "s"], [2]) is False
    assert W.letter_match(["c", "a", "k", "e", "s"], [3]) is False
    assert W.letter_match(["c", "a", "k", "e", "s"], [4]) is False

    assert W.letter_match(["c", "a", "k", "e", "d"], [2]) is True # This works for any index but 4 which is good
    assert W.letter_match(["c", "r", "u", "s", "t"], [0]) is True
    assert W.letter_match(["f", "r", "i", "e", "d"], [1]) is True
    assert W.letter_match(["a", "b", "i", "d", "e"], [2]) is True
    assert W.letter_match(["c", "a", "n", "d", "y"], [3]) is True
    assert W.letter_match(["p", "h", "o", "n", "y"], [4]) is True

test_valid_words_letter_match()

