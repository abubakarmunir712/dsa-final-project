from classes.sequence import Sequence
from typing import List
from classes.card import Card


# Player
class Player:

    # Constructor
    def __init__(self, cards: List[Card], name="Unknown", is_AI=False, game_id=None):
        self.__hand = [None] * 5
        self.populate_sequences(cards)
        self.__name = name
        self.__points = 0
        self.__is_AI = is_AI
        self.__game_id = game_id
        self.__has_first_life = False
        self.__has_second_life = False

    # Getters for attributes
    def get_name(self):
        return self.__name

    def get_hand(self):
        return self.__hand

    def get_points(self):
        return self.__points

    def get_is_AI(self):
        return self.__is_AI

    def get_game_id(self):
        return self.__game_id

    # Populate hand of player
    def populate_sequences(self, cards: List[Card]):
        # Seperate cards of same suit
        self.hearts = []
        self.spades = []
        self.diamonds = []
        self.clubs = []
        self.joker = []

        for i in range(len(cards)):
            if cards[i].get_suit() == "hearts":
                self.hearts.append(cards[i])
            elif cards[i].get_suit() == "spades":
                self.spades.append(cards[i])
            elif cards[i].get_suit() == "clubs":
                self.clubs.append(cards[i])
            elif cards[i].get_suit() == "diamonds":
                self.diamonds.append(cards[i])
            else:
                self.joker.append(cards[i])

        suits_array = [self.hearts, self.spades, self.diamonds, self.clubs, self.joker]
        for i in range(5):
            self.__hand[i] = Sequence(suits_array[i])
