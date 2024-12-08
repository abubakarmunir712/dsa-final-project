from utility.utility import bubble_sort, insertion_sort


# Sequence
class Sequence:
    def __init__(self, cards):
        self.__cards = cards
        self.__sequence = self.calculate_sequence(cards)

    # Calculating the sequence type of the cards
    def calculate_sequence(self, first_life, second_life):
        __cards = bubble_sort(__cards)

    # Getters for attributes
    def get_sequence(self):
        return self.__sequence

    def get_cards(self):
        return self.__cards
