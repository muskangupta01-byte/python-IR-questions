import random

class Dictionary:
    def __init__(self, words):
        # words: list of equal-length uppercase strings
        self.words = words

    def get_random(self):
        return random.choice(self.words)
