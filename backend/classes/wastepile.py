from typing import List
from classes.card import Card
from data_structures.stack import Stack


class WastePile:
    # Initialize pile with cards
    def __init__(self, cards: List[Card]):
        self.pile = Stack()
        for card in cards:
            self.pile.push(card)

    # Get top card
    def get_card(self):
        if self.pile.get_top().is_joker():
            return None
        else:
            return self.pile.pop()
