from classes.sequence import Sequence
from typing import List
from classes.card import Card
from enums.status_enum import Status


# Player
class Player:

    # Constructor
    def __init__(self, cards: List[Card], name="Unknown", is_AI=False, game_id=None):
        self.__hand = [None] * 5
        self.__name = name
        self.__points = 0
        self.__is_AI = is_AI
        self.__game_id = game_id
        self.has_first_life = False
        self.has_second_life = False
        self.populate_sequences(cards)

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
            self.__hand[i] = Sequence(
                suits_array[i], self.has_first_life, self.has_second_life
            )

    # Check if player has first life and second life
    def check_sequence_status(self):
        for i in range(5):
            if self.__hand[i] != None:
                if self.__hand[i].get_sequence_status() == Status.FIRST_LIFE.value:
                    self.has_first_life = True
                elif self.__hand[i].get_sequence_status() == Status.SECOND_LIFE.value:
                    self.has_second_life = True

    def play(self):
        if self.__is_AI:
            pass
        else:
            pass

    def move_card(self, sequence_number_1, sequence_number_2, card_name):
        # Sequence no 1 represent seq from where card is being removed
        # Sequence no 2 represent seq from where card is being added
        if (
            sequence_number_1 < 0
            or sequence_number_1 > 4
            or sequence_number_2 < 0
            or sequence_number_2 > 4
        ):
            return False
        card = self.__hand[sequence_number_1].remove_card_from_sequence(card_name)
        if (
            card is not None
            and self.__hand[sequence_number_2].get_number_of_cards() != 0
        ):
            self.__hand[sequence_number_2].insert_card_into_sequence(card)
            return True
        return False

    # Make a group of cards
    def group_cards(self, cards_list):
        # Format of card_list = list of tuples in this format (sequence_number, "card_name")
        self.cards_list = []
        for card in cards_list:
            if card[0] < 5 and card[0] >= 0:
                card = self.__hand[card[0]].remove_card_from_sequence(card[1])
                if card is not None:
                    self.cards_list.append(card)
                else:
                    return False
            else:
                return False

        # Insert cards into first empty sequence (if any)
        for i in range(5):
            if self.__hand[i].get_number_of_cards() == 0:
                self.__hand[i] = Sequence(
                    self.cards_list, self.has_first_life, self.has_second_life
                )
                return True

        # If no sequence is empty append it to last sequence
        self.__hand[4] = Sequence(
            self.cards_list, self.has_first_life, self.has_second_life
        )
        return True
