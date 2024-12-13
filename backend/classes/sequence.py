from utility.utilities import bubble_sort, find_max_rank, find_min_rank
from enums.status_enum import Status
from classes.card import Card
from typing import List, Optional
from data_structures.hashmap import HashMap


# Sequence
class Sequence:
    def __init__(
        self, cards: Optional[List[Card]] = None, first_life=False, second_life=False
    ):
        self.__cards = cards
        self.__sequence_status = None
        self.check_status(first_life, second_life)

    # Check the status of the sequence
    def check_status(self, first_life, second_life):
        # If the sequence is empty
        if len(self.__cards) == 0:
            self.__sequence_status == None
            return

        # If the sequence has less than 3 cards
        if len(self.__cards) < 3:
            self.__sequence_status = Status.INVALID
            return

        # Sort cards according to their rank
        self._cards = bubble_sort(self.__cards)

        # Get all jokers (both printed and wild jokers)
        self.wild_jokers = [
            index
            for index, card in enumerate(self.__cards)
            if (card.is_joker() and card.get_rank != 0)
        ]
        self.printed_jokers = [
            index for index, card in enumerate(self.__cards) if card.get_rank() == 0
        ]

        self.jokers = self.get_jokers()
        if not first_life and not second_life:
            if self.is_pure_sequence():
                self.__sequence_status = Status.FIRST_LIFE
            elif self.is_impure_sequence():
                self.__sequence_status = Status.FIRST_LIFE_REQUIRED
            elif self.is_set():
                self.__sequence_status = Status.SECOND_LIFE_REQUIRED
            else:
                self.__sequence_status = Status.INVALID

        elif first_life and not second_life:
            if self.is_pure_sequence():
                self.__sequence_status = Status.SECOND_LIFE
            elif self.is_impure_sequence():
                self.__sequence_status = Status.SECOND_LIFE
            elif self.is_set():
                self.__sequence_status = Status.SECOND_LIFE_REQUIRED
            else:
                self.__sequence_status = Status.INVALID
        elif first_life and second_life:
            if self.is_pure_sequence():
                self.__sequence_status = Status.PURE_SEQUENCE
            elif self.is_impure_sequence():
                self.__sequence_status = Status.IMPURE_SEQUENCE
            elif self.is_set():
                self.__sequence_status = Status.SET
            else:
                self.__sequence_status = Status.INVALID
        return self.__sequence_status

    # Check if a sequence is pure sequence
    def is_pure_sequence(self) -> bool:
        self.jokers = self.get_jokers()
        self.toggle_ace_rank_value(True)
        # If sequence contains printed jokers it can't be pure
        if (
            len(self.jokers[0]) != 0
            or self.calculate_rank_difference(self.__cards) != 0
        ):
            return False
        else:
            return True

    # Check if a sequence is impure sequence
    def is_impure_sequence(self) -> bool:
        self.jokers = self.get_jokers()
        self.toggle_ace_rank_value(False)
        self.total_jokers = len(self.jokers[0]) + len(self.jokers[1])
        self.cards_without_jokers = [
            cards
            for index, cards in enumerate(self.__cards)
            if index not in self.jokers[0] and index not in self.jokers[1]
        ]
        self.rank_difference = self.calculate_rank_difference(self.cards_without_jokers)
        if self.rank_difference != -1 and self.total_jokers >= self.rank_difference:
            return True
        else:
            return False

    # Check if sequence is a set
    def is_set(self):
        self.jokers = self.get_jokers()
        # Set can contain at most 4 cards otherwise suit will start repeating
        if len(self.__cards) > 4:
            return False
        self.rank = self.__cards[0].rank[:1]
        self.suit = HashMap(10)
        for index, card in enumerate(self.__cards):
            if index in self.jokers[0] or index in self.jokers[1]:
                continue
            if card.rank[:1] == self.rank:
                if self.suit.get(card.get_suit()) == True:
                    return False
                else:
                    self.suit.insert(card.get_suit())
            else:
                return False
        return True

    # Calculate
    def calculate_rank_difference(self, cards: List[Card]):
        cards = bubble_sort(cards)
        self.rank_difference = 0
        self.suit = cards[0].get_suit()
        # Create hashmap to check if
        self.rank = HashMap(10)
        self.rank.insert(cards[0].card_name)
        for i in range(1, len(cards)):
            if (
                cards[i].get_suit() == self.suit
                and self.rank.get(cards[i].card_name) == None
            ):
                self.rank_difference += abs(
                    cards[i].get_rank() - (cards[i - 1].get_rank() + 1)
                )
                self.rank.insert(cards[i].card_name)
            else:
                return -1
        return self.rank_difference

    # Toggle ace value
    def toggle_ace_rank_value(self, checking_for_pure_sequence):
        self.max_rank = find_max_rank(self.__cards, checking_for_pure_sequence)
        self.min_rank = find_min_rank(self.__cards, checking_for_pure_sequence)

        if 14 - self.max_rank > self.min_rank - 1:
            self.desired_rank = 1
        else:
            self.desired_rank = 14

        for card in self.__cards:
            if (
                card.rank != None
                and card.rank[:1] == "A"
                and card.get_rank() != self.desired_rank
            ):
                card.toggle_ace_rank()

    # Getters for attributes
    def get_sequence_status(self):
        if self.__sequence_status == None:
            return None
        return self.__sequence_status.value

    def get_cards(self):
        return self.__cards

    # Get all jokers in set
    def get_jokers(self):
        self.wild_jokers = [
            index
            for index, card in enumerate(self.__cards)
            if (card.is_joker() and card.get_rank != 0)
        ]
        self.printed_jokers = [
            index for index, card in enumerate(self.__cards) if card.get_rank() == 0
        ]

        return (self.printed_jokers, self.wild_jokers)

    # Get total points of sequence
    def get_points(self) -> int:
        if (
            self.__sequence_status == Status.FIRST_LIFE
            or self.__sequence_status == Status.SECOND_LIFE
            or self.__sequence_status == Status.SET
            or self.__sequence_status == None
        ):
            return 0
        else:
            self.total_points = 0
            for card in self.__cards:
                self.total_points += card.get_points()
            return self.total_points

    def get_number_of_cards(self):
        return len(self.__cards)

    # Remove a card from sequence
    def remove_card_from_sequence(self, card_name) -> Card:
        self.index = None
        for i in range (len(self.__cards)):
            if self.__cards[i].card_name == card_name:
                self.index = i
                break
        if self.index is not None:
            return self.__cards.pop(self.index)
        return None

    # Insert a card into sequence
    def insert_card_into_sequence(self, card):
        self.__cards.append(card)
        return True
