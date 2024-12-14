from typing import List, Tuple
from classes.card import Card
from classes.player import Player
from classes.stockpile import StockPile
from classes.wastepile import WastePile

class Bot(Player):
    def _init_(self, hand: List[Card], stock_pile: StockPile, waste_pile: WastePile):
        self.hand = hand
        self.stock_pile = stock_pile
        self.waste_pile = waste_pile

    def analyze_hand(self) -> Tuple[List[List[Card]], List[List[Card]]]:
        """Analyze hand to find potential sequences or sets."""
        sequences, sets = [], []
        suits = {}

        for card in self.hand:
            suits.setdefault(card.suit, []).append(card)

        # Find sequences
        for suit, cards in suits.items():
            cards.sort(key=lambda c: c.get_rank())
            temp_seq = []

            for i in range(len(cards) - 1):
                if cards[i + 1].get_rank() - cards[i].get_rank() == 1:
                    temp_seq.append(cards[i])
                else:
                    if len(temp_seq) >= 2:
                        temp_seq.append(cards[i])  # Include the last card
                        sequences.append(temp_seq)
                    temp_seq = []
            if len(temp_seq) >= 2:
                temp_seq.append(cards[-1])
                sequences.append(temp_seq)

        # Find sets
        rank_groups = {}
        for card in self.hand:
            rank_groups.setdefault(card.rank, []).append(card)

        for rank, group in rank_groups.items():
            if len(group) >= 3:
                sets.append(group)

        return sequences, sets

    def make_move(self) -> str:
        for i in range(len(self.hand)):
            print(self.hand[i].card_name)
        """Decide and make the best move."""
        sequences, sets = self.analyze_hand()

        if not sequences and not sets:
            # No sequences or sets, draw a card from the stockpile
            drawn_card = self.stock_pile.dequeue()
            self.hand.append(drawn_card)
            return f"Drew card {drawn_card.card_name} from stockpile."

        # Attempt to discard a card that's least useful
        for card in self.hand:
            if not self.is_card_useful(card, sequences, sets):
                self.hand.remove(card)
                self.waste_pile.push(card)
                return f"Discarded card {card.card_name} to wastepile."

        # Default action: discard the card with the lowest rank
        lowest_card = min(self.hand, key=lambda c: c.get_rank())
        self.hand.remove(lowest_card)
        self.waste_pile.push(lowest_card)
        return f"Discarded card {lowest_card.card_name} to wastepile."

    def is_card_useful(self, card: Card, sequences: List[List[Card]], sets: List[List[Card]]) -> bool:
        """Determine if a card is part of a useful sequence or set."""
        for sequence in sequences:
            if card in sequence:
                return True
        for set_group in sets:
            if card in set_group:
                return True
        return False