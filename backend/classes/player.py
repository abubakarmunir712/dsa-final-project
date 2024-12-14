from classes.sequence import Sequence
from typing import List
from classes.card import Card
from enums.status_enum import Status
from classes.stockpile import StockPile
from classes.wastepile import WastePile


# Player
class Player:

    # Constructor
    def __init__(self, cards: List[Card], name="Unknown", is_AI=False, player_id=None):
        self.hand = [None] * 5
        self.name = name
        self.points = 0
        self.is_AI = is_AI
        self.player_id = player_id
        self.has_first_life = False
        self.has_second_life = False
        self.populate_sequences(cards)

    # Getters for attributes
    def get_name(self):
        return self.name

    def get_hand(self):
        return self.hand

    def get_points(self):
        if self.points > 80:
            return 80
        return self.points

    def get_is_AI(self):
        return self.is_AI

    def get_player_id(self):
        return self.player_id

    # Populate hand of player
    def populate_sequences(self, cards: List[Card]):
        # Seperate cards of same suit
        self.hearts = []
        self.spades = []
        self.diamonds = []
        self.clubs = []
        self.joker = []

        for i in range(len(cards)):
            if cards[i].get_suit() is None:
                self.joker.append(cards[i])
            elif cards[i].get_suit().lower() == "hearts":
                self.hearts.append(cards[i])
            elif cards[i].get_suit().lower() == "spades":
                self.spades.append(cards[i])
            elif cards[i].get_suit().lower() == "clubs":
                self.clubs.append(cards[i])
            elif cards[i].get_suit().lower() == "diamonds":
                self.diamonds.append(cards[i])

        suits_array = [self.hearts, self.spades, self.diamonds, self.clubs, self.joker]
        for i in range(5):
            self.hand[i] = Sequence(
                suits_array[i], self.has_first_life, self.has_second_life
            )
        self.check_sequence_status()
        self.calulate_points()

    # Calculate points of player
    def calulate_points(self):
        self.points = 0
        for i in range(5):
            self.points += self.hand[i].get_points()

    # Check if player has first life and second life
    def check_sequence_status(self):
        self.has_first_life = False
        self.has_second_life = False
        self.first_life_index = -1
        self.second_life_index = -1
        for j in range(3):
            for i in range(5):
                if i == self.first_life_index or i == self.second_life_index:
                    continue
                if self.hand[i] != None:
                    # Check if sequence is first life
                    if (
                        self.hand[i].check_status(
                            self.has_first_life, self.has_second_life
                        )
                        == Status.FIRST_LIFE
                    ):
                        self.has_first_life = True
                        self.first_life_index = i

                    # Check if sequence is second life
                    elif (
                        self.hand[i].check_status(
                            self.has_first_life, self.has_second_life
                        )
                        == Status.SECOND_LIFE
                    ):
                        self.has_second_life = True
                        self.second_life_index = i

    def move_card(self, sequence_number_1, sequence_number_2, card_name) -> bool:
        # Sequence no 1 represent seq from where card is being removed
        # Sequence no 2 represent seq from where card is being added
        if (
            sequence_number_1 < 0
            or sequence_number_1 > 4
            or sequence_number_2 < 0
            or sequence_number_2 > 4
        ):
            return False
        self.card = self.hand[sequence_number_1].remove_card_from_sequence(card_name)
        if self.card is not None:
            self.hand[sequence_number_2].insert_card_into_sequence(self.card)
            self.check_sequence_status()
            return True
        return False

    # Make a group of cards
    def group_cards(self, cards_list) -> bool:
        # Format of card_list = list of tuples in this format (sequence_number, "card_name")
        self.cards_list = []
        for card in cards_list:
            if card[0] < 5 and card[0] >= 0:
                self.card = self.hand[card[0]].remove_card_from_sequence(card[1])
                if self.card is not None:
                    self.cards_list.append(self.card)
            else:
                return False

        # Insert cards into first empty sequence (if any)
        for i in range(5):
            if self.hand[i].get_number_of_cards() == 0:
                self.hand[i] = Sequence(
                    self.cards_list, self.has_first_life, self.has_second_life
                )
                self.check_sequence_status()
                return True

        # If no sequence is empty append it to last sequence
        for card in self.cards_list:
            self.hand[4].insert_card_into_sequence(card)
        self.check_sequence_status()
        return True

    # Getting card from waste pile
    def get_card_from_wastepile(self, pile: WastePile) -> bool:
        self.card = pile.get_card()
        if self.card is None:
            return False
        self.hand[4].insert_card_into_sequence(self.card)
        self.check_sequence_status()
        return True

    # Get card from stock pile
    def get_card_from_stockpile(self, pile: StockPile) -> bool:
        self.card = pile.get_card()
        if self.card is not None:
            self.hand[4].insert_card_into_sequence(self.card)
            self.check_sequence_status()
            return True
        return False

    # Move card to waste pile
    def discard_card(self, sequence_no, card_name, pile: WastePile):
        self.card = self.hand[sequence_no].remove_card_from_sequence(card_name)
        if self.card is not None:
            pile.insert_card(self.card)
            return True
        return False
