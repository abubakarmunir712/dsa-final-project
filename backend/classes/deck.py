from classes.card import Card
from typing import List
import random


# Deck
class Deck:
    # Constructor
    def __init__(self):
        self.cards: List[Card] = []
        self.__ranks = [
            "A",
            "K",
            "Q",
            "J",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
        ]
        self.__suits = ["hearts", "diamonds", "spades", "clubs"]
        self.initialize_deck(self.__ranks, self.__suits)
        self.joker = self.make_joker()
        self.shuffle()

    # Initialize deck
    def initialize_deck(self, ranks, suits):
        # Suits and ranks of the cards

        # Adding 2 sets of 52 cards to ensure the game logic
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.cards.append(card)
                self.cards.append(card)

        # Add 4 jokers
        for _ in range(4):
            self.cards.append(Card(None, None, True))

    # Shuffle deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Draw card
    def draw_card(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    # Make joker
    def make_joker(self):
        joker_rank = random.choice(self.__ranks)
        for card in self.cards:
            if card.is_joker():
                continue
            if card.rank == joker_rank:
                card.make_joker()
        return joker_rank

    # Get all cards
    def get_all_cards(self):
        return self.cards
