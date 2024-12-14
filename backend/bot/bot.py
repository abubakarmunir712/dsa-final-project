from typing import List
from classes.card import Card
from enums.status_enum import Status
from classes.player import Player
from classes.stockpile import StockPile
from classes.wastepile import WastePile
from data_structures.graph import Graph
from classes.sequence import Sequence

class AIPlayer(Player):
    def __init__(self, cards: List[Card], name="AI Player", is_AI=True, player_id=None):
        super().__init__(cards, name, is_AI, player_id)
        self.graph = Graph()  # Initialize a graph for the AI's cards

    def play(self, stock_pile: StockPile, waste_pile: WastePile) -> bool:
        """
        The method where the AI makes its move. AI decides whether to draw from StockPile or WastePile,
        tries to group cards into sequences, and discards unwanted cards.
        """
        print(f"{self.get_name()} is making its move.")

        # Step 1: Decide whether to draw a card from the StockPile or WastePile
        drawn_card = None
        if waste_pile.is_empty():
            drawn_card = self.get_card_from_stockpile(stock_pile)
            print(f"{self.get_name()} drew a card from the StockPile.")
        else:
            drawn_card = self.get_card_from_wastepile(waste_pile)
            print(f"{self.get_name()} drew a card from the WastePile.")
        
        if not drawn_card:
            return False

        # Step 2: Add the drawn card to the graph and check sequences
        self.add_card_to_graph(drawn_card)
        self.group_cards_using_graph()

        # Step 3: If sequence size exceeds 5, discard a card
        if self.get_hand()[4].get_number_of_cards() > 5:  # Example condition, max cards in a sequence is 5
            card_name_to_discard = self.decide_card_to_discard()
            if card_name_to_discard:
                self.discard_card(4, card_name_to_discard, waste_pile)
                print(f"{self.get_name()} discarded {card_name_to_discard} to the WastePile.")

        # Step 4: Check for winning condition or if the AI needs to end its turn
        self.check_sequence_status()
        if self.has_won():
            print(f"{self.get_name()} has won the game!")
            return True  # AI wins the game
        
        return False  # AI's turn is over, game continues

    def add_card_to_graph(self, card: Card) -> None:
        """
        Add the drawn card to the AI's graph and connect it to other cards in the hand
        that can form valid sequences with it.
        """
        for sequence in self.get_hand():
            # Check if the sequence is a valid Sequence object and contains cards
            if isinstance(sequence, Sequence):
                for existing_card in sequence.get_cards():  # Loop over the cards in the sequence
                    if self.is_valid_sequence(existing_card, card):  # Check if the two cards can form a valid sequence
                        self.graph.add_edge(existing_card.card_name, card.card_name)
        self.graph.add_edge(card.card_name, card.card_name)  # A card is always connected to itself

    def group_cards_using_graph(self) -> None:
        """
        Group cards into sequences based on the graph, finding all connected components.
        """
        visited = set()
        for sequence in self.get_hand():
            # Ensure we're dealing with valid sequences
            if isinstance(sequence, Sequence):
                for card in sequence.get_cards():
                    if card.card_name not in visited:
                        connected_sequence = self.graph.get_sequence_from_card(card.card_name)
                        # Create a sequence with the found cards
                        self.create_or_update_sequence(connected_sequence, visited)

    def create_or_update_sequence(self, sequence: List[str], visited: set) -> None:
        """
        Create a new sequence or update an existing sequence with the cards from the graph traversal.
        """
        if len(sequence) >= 3:  # Only consider valid sequences with at least 3 cards
            sequence_obj = Sequence(sequence, Status.PURE_SEQUENCE)
            self.hand.append(sequence_obj)  # Add the sequence to the AI's hand
            for card_name in sequence:
                visited.add(card_name)

    def is_valid_sequence(self, card1: Card, card2: Card) -> bool:
        """
        Check if two cards can form a valid sequence (e.g., consecutive numbers of the same suit).
        """
        return card1.card_suit == card2.card_suit and abs(card1.card_number - card2.card_number) == 1

    def decide_card_to_discard(self) -> str:
        """
        The AI decides which card to discard.
        For simplicity, it discards the first card in the sequence (this can be more complex).
        """
        if self.get_hand()[4].get_number_of_cards() > 0:
            card_name = self.get_hand()[4].get_cards()[0].card_name
            return card_name
        return None

    def has_won(self) -> bool:
        """
        Check if the AI has won the game by having at least one valid sequence.
        """
        valid_sequences = sum(1 for sequence in self.get_hand() if isinstance(sequence, Sequence) and sequence.get_sequence_status() == Status.PURE_SEQUENCE)
        return valid_sequences >= 1  # Modify based on the actual game rules

    def get_card_from_wastepile(self, pile: WastePile) -> bool:
        """
        AI picks a card from the WastePile if available.
        """
        self.card = pile.get_card()
        if self.card is None:
            return False
        self.hand[4].insert_card_into_sequence(self.card)
        self.check_sequence_status()
        return True

    def get_card_from_stockpile(self, pile: StockPile) -> bool:
        """
        AI picks a card from the StockPile if available.
        """
        self.card = pile.get_card()
        if self.card is not None:
            self.hand[4].insert_card_into_sequence(self.card)
            self.check_sequence_status()
            return True
        return False

    def discard_card(self, sequence_no, card_name, pile: WastePile):
        """
        AI discards a card from its sequence to the WastePile.
        """
        self.card = self.hand[sequence_no].remove_card_from_sequence(card_name)
        if self.card is not None:
            pile.insert_card(self.card)
            return True
        return False

    def check_sequence_status(self):
        """
        This method can be used to check and update the status of sequences after each move.
        You can mark sequences as valid, invalid, or incomplete here.
        """
        for sequence in self.get_hand():
            if isinstance(sequence, Sequence):
                sequence.update_status()  # Example of checking if the sequence is valid after a move

    def get_hand(self) -> List[Sequence]:
        """
        Returns the current hand, which is a list of Sequence objects.
        Each Sequence contains a list of Card objects.
        """
        return self.hand
