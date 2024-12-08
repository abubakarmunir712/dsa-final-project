from classes.card import Card
import random


# Deck
class Deck:
    # Constructor
    def __init__(self):
        self.cards = []
        self.initialize_deck()
        self.shuffle()

    # Initialize deck
    def initialize_deck(self):
        # Suits and ranks of the cards
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        ranks = ["A", "K", "Q", "J", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

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
