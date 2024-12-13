from enums.rank_enum import Rank
from enums.suit_enum import Suit


# Card
class Card:
    def __init__(self, suit, rank, is_joker=False):
        # Ensure is_joker is set to true when both suit and rank are none
        if (suit == None) and (rank == None) and (is_joker == False):
            is_joker = True

        # Ensure that either both suit and rank are None or both are not None
        if (suit is None) ^ (rank is None):
            raise ValueError(
                "If one of the suit or rank is None, the other must also be None."
            )

        # Check if suit is valid
        if suit is None or self._is_valid_suit(suit):
            self.suit = suit
        else:
            raise ValueError(
                f"{suit} is not a valid suit. Valid suits include hearts, diamonds, spades, clubs and None (in case of joker)"
            )

        # Check if rank is valid
        if rank is None or self._is_valid_rank(rank):
            self.rank = rank
        else:
            raise ValueError(
                f"{rank} is not a valid rank. Valid ranks include A, K, Q, J, None (in case of joker) and numbers from 2 to 10."
            )

        self.visible = False
        self.joker = is_joker
        if suit is None:
            self.card_name = "joker"
        else:
            self.card_name = self.suit + "__" + self.rank[:1]

    def _is_valid_rank(self, input_rank):
        return input_rank.upper() in [rank.value for rank in Rank]

    def _is_valid_suit(self, input_suit):
        return input_suit.lower() == input_suit.lower() in [suit.value for suit in Suit]

    def get_suit(self):
        return self.suit

    def is_visible(self):
        return self.visible

    def is_joker(self):
        return self.joker

    def make_joker(self):
        self.joker = True

    def get_points(self):
        if self.joker:
            return 0
        elif self.rank == "A" or self.rank == "A+":
            return 20
        elif self.rank == "K" or self.rank == "Q" or self.rank == "J":
            return 10
        else:
            return int(self.rank)

    def toggle_ace_rank(self):
        if self.rank == "A":
            self.rank = "A+"
            return True
        elif self.rank == "A+":
            self.rank = "A"
            return True
        else:
            return False

    def get_rank(self):
        if self.rank == "A":
            return 1
        elif self.rank == "A+":
            return 14
        elif self.rank == "J":
            return 11
        elif self.rank == "Q":
            return 12
        elif self.rank == "K":
            return 13
        elif self.rank == None and self.rank == None:
            return 0  # In case of printed joker
        else:
            return int(self.rank)
