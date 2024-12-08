from backend.utility.utilities import bubble_sort
import enum


class Status(enum):
    SET = "set"
    INVALID = "invalid"
    FIRST_LIFE = "first_life"
    SECOND_LIFE = "second_life"
    PURE_SEQUENCE = "pure_sequence"
    IMPURE_SEQUENCE = "impure_sequence"
    FIRST_LIFE_REQUIRED = "first_life_required"
    SECOND_LIFE_REQUIRED = "second_life_requred"


# Sequence
class Sequence:
    def __init__(self, cards=None, first_life=False, second_life=False):
        self.__cards = cards
        self.__sequence_status = None
        self.calculate_sequence(first_life, second_life)

    # Calculating the sequence type of the cards
    def calculate_sequence(self, first_life, second_life):
        # If the sequence is empty
        if len(self.__cards) == 0:
            self.__sequence_status == None
            return

        # If the sequence has less than 3 cards
        if len(self.__cards) < 3:
            self.__sequence_status = Status.INVALID
            return

        # In start sequence is invalid
        self.__sequence_status = Status.INVALID

        # Sorting the cards for easy comparison
        self.__cards = bubble_sort(self.__cards)

        # If first life does not exist
        if not first_life:
            if self.is_pure_sequence():
                self.__sequence_status = Status.FIRST_LIFE
                return

        # If second life does not exist
        if not second_life and first_life:
            if self.is_impure_sequence():
                self.__sequence_status = Status.SECOND_LIFE
                return

        # If first and second life already exists then check for the pure sequence
        if self.is_pure_sequence():
            self.__sequence_status = Status.PURE_SEQUENCE
            return

    # Checking pure sequence (Checks first life because first life is a pure sequence)
    def is_pure_sequence(self):
        if not self.check_ace_rank_validity():
            False

        for i in range(len(self.__cards) - 1):
            if not self.check_suit_rank(self.__cards[i], self.__cards[i + 1]):
                return False
            if self.__cards[i].is_joker() or self.__cards[i + 1].is_joker():
                return False

        return True

    # Checking second life (Second life can also be an impure sequence so checking the suit and rank only)
    def is_impure_sequence(self):
        if not self.check_ace_rank_validity():
            False

        for i in range(len(self.__cards) - 1):
            if not self.check_suit_rank(self.__cards[i], self.__cards[i + 1]):
                return False

        return True

    # Checks the ace validity such that the ace can be used as 1 or 14 for different conditions
    def check_ace_rank_validity(self):
        if (
            self.__cards[0].get_rank() == 1
            and self.__cards[1].get_rank() == 2
            and self.__cards[len(self.__cards) - 1].get_rank() == 13
        ):
            return False

        if (
            self.__cards[0].get_rank() == 1
            and self.__cards[len(self.__cards) - 1].get_rank() == 13
        ):
            self.__cards[0].toggle_ace_rank()
            self.__cards = self.bubble_sort(self.__cards)

        if (
            self.__cards[0].get_rank() == 2
            and self.__cards[len(self.__cards) - 1].get_rank() == 14
        ):
            self.__cards[len(self.__cards) - 1].toggle_ace_rank()
            self.__cards = self.bubble_sort(self.__cards)

        return True

    # Checking if the suit and rank are valid for pure sequence
    def check_suit_rank(self, card1, card2):
        if not card1.get_suit() == card2.get_suit():
            return False
        if not card1.get_rank() == card2.get_rank() - 1:
            return False

        return True

    # Getters for attributes
    def get_sequence(self):
        return self.__sequence_status

    def get_cards(self):
        return self.__cards
