from typing import List
from classes.card import Card
from data_structures.queue import Queue


class StockPile:
    # Initialize pile with cards
    def __init__(self, cards: List[Card]):
        self.pile = Queue()
        for card in cards:
            self.pile.enqueue(card)

    # Get top card
    def get_card(self):
        return self.pile.dequeue()
