# WordRules
# defines all the possible rules/restrictions for a word

#    not sure exactly how this should be structured/operated yet. 
#    But seems like it may be a good idea to seperate rules to their own file
#    so we can more easily add additional rules and such, and keep things readable
#
#    could be merged with GameManager if it turns out there isnt good enough reason to seperate

# TODO: Implement WordRules
import string
class WordRules:
    def __init__(self):
        try:
            file = open('words.txt')
        except FileNotFoundError:
            print('ERROR: File not found')
        else:
            self._word_list = [word.strip().lower() for word in file if len(word.strip()) == 5 and string.punctuation not in word]
            file.close()

    
    def contains_letters(letters: list[str]):
        pass