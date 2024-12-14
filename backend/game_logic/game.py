import uuid
from data_structures.queue import Queue
from data_structures.stack import Stack
from classes.deck import Deck
from classes.player import Player


# Game
class Game:
    # Constructor
    def __init__(self, no_of_players=1, no_ai_players=1):
        self.game_id = str(uuid.uuid4())  # Generate a unique game ID
        self.stock_pile = Queue()  # Stock pile
        self.waste_pile = Stack()  # Waste pile
        self.deck = Deck()  # Deck
        self.players = Queue()  # Players
        self.initialize_game(no_of_players, no_ai_players)  # Initialize game

    # Initializing game
    def initialize_game(self, no_of_players, no_ai_players):
        id = 0
        # Initializing human players
        for i in range(0, no_of_players):
            cards = []
            # Dealing cards to each player
            for _ in range(13):
                cards.append(self.deck.draw_card())
            player = Player(cards, False, id)
            self.players.enqueue(player)
            print(id)
            id += 1

        # Initializing AI players
        for i in range(no_ai_players):
            cards = []
            # Dealing cards to each player
            for _ in range(13):
                cards.append(self.deck.draw_card())
            player = Player(cards, f"AI-Player {i}", True, id)
            self.players.enqueue(player)
            id += 1

        # Dealing remaining cards to the stock pile
        while self.deck.cards:
            self.stock_pile.enqueue(self.deck.draw_card())
