from classes.card import Card
from enums.status_enum import Status
from typing import List, Dict, Tuple
from utility.utilities import bubble_sort
import networkx as nx

class RummyBot:
    def __init__(self, player):
        self.player = player
        self.graph = nx.DiGraph()  # Directed graph to represent card arrangements

    def play_turn(self, draw_pile: List[Card], discard_pile: List[Card]):
        """
        Main bot function to handle the player's turn.
        :param draw_pile: List of cards available to draw.
        :param discard_pile: List of cards in the discard pile.
        """
        # Analyze the current hand
        hand = self.player.get_hand()

        # Step 1: Analyze the best move
        best_move = self.evaluate_best_move(hand, discard_pile)

        # Step 2: Execute the move
        if best_move == "DRAW_DISCARD":
            drawn_card = discard_pile.pop()
            self.player.add_card_to_hand(drawn_card)
        else:
            drawn_card = draw_pile.pop()
            self.player.add_card_to_hand(drawn_card)

        # Step 3: Evaluate discard
        discard_card = self.select_discard_card(self.player.get_hand())
        self.player.remove_card_from_hand(discard_card.card_name)
        discard_pile.append(discard_card)

        return "TURN_COMPLETE"

    def evaluate_best_move(self, hand: List[Card], discard_pile: List[Card]) -> str:
        """
        Decide whether to draw from the discard pile or the draw pile.
        :param hand: The player's current hand.
        :param discard_pile: The discard pile to evaluate.
        :return: "DRAW_DISCARD" or "DRAW_PILE"
        """
        if not discard_pile:
            return "DRAW_PILE"

        top_discard = discard_pile[-1]
        potential_hand = hand + [top_discard]

        if self.can_form_sequence(potential_hand) or self.can_form_set(potential_hand):
            return "DRAW_DISCARD"

        return "DRAW_PILE"

    def select_discard_card(self, hand: List[Card]) -> Card:
        """
        Select the best card to discard from the hand.
        :param hand: The player's current hand.
        :return: The selected card to discard.
        """
        # Prioritize discarding high-point cards that don't help in sequences or sets
        non_useful_cards = [card for card in hand if not self.is_useful_card(card, hand)]

        # If no obvious non-useful cards, randomly discard a high-point card
        if non_useful_cards:
            non_useful_cards.sort(key=lambda card: card.get_points(), reverse=True)
            return non_useful_cards[0]

        # Default to discarding the highest point card
        hand.sort(key=lambda card: card.get_points(), reverse=True)
        return hand[0]

    def can_form_sequence(self, hand: List[Card]) -> bool:
        """
        Check if the hand can form or extend a sequence.
        :param hand: The player's current hand.
        :return: True if a sequence can be formed, False otherwise.
        """
        sorted_hand = bubble_sort(hand)
        jokers = [card for card in sorted_hand if card.is_joker()]
        non_jokers = [card for card in sorted_hand if not card.is_joker()]

        for i in range(len(non_jokers) - 2):
            if (
                non_jokers[i + 1].get_rank() == non_jokers[i].get_rank() + 1
                and non_jokers[i + 2].get_rank() == non_jokers[i + 1].get_rank() + 1
            ):
                return True

        # Check for impure sequence with jokers
        if len(non_jokers) + len(jokers) >= 3:
            return True

        return False

    def can_form_set(self, hand: List[Card]) -> bool:
        """
        Check if the hand can form or extend a set.
        :param hand: The player's current hand.
        :return: True if a set can be formed, False otherwise.
        """
        rank_count = {}
        for card in hand:
            rank = card.get_rank()
            if rank not in rank_count:
                rank_count[rank] = 0
            rank_count[rank] += 1

        for count in rank_count.values():
            if count >= 3:
                return True

        return False

    def is_useful_card(self, card: Card, hand: List[Card]) -> bool:
        """
        Determine if a card is useful for forming sequences or sets.
        :param card: The card to evaluate.
        :param hand: The player's current hand.
        :return: True if the card is useful, False otherwise.
        """
        temp_hand = hand.copy()
        temp_hand.remove(card)

        if self.can_form_sequence(temp_hand) or self.can_form_set(temp_hand):
            return True

        return False

    def build_graph(self, hand: List[Card]):
        """
        Build a graph representing possible sequences and sets from the hand.
        :param hand: The player's current hand.
        """
        self.graph.clear()
        for card in hand:
            self.graph.add_node(card.card_name, rank=card.get_rank(), suit=card.get_suit())

        # Add edges for possible sequences
        for i in range(len(hand)):
            for j in range(i + 1, len(hand)):
                if abs(hand[i].get_rank() - hand[j].get_rank()) == 1:
                    self.graph.add_edge(hand[i].card_name, hand[j].card_name, type="sequence")

        # Add edges for possible sets
        rank_groups = {}
        for card in hand:
            rank = card.get_rank()
            if rank not in rank_groups:
                rank_groups[rank] = []
            rank_groups[rank].append(card)

        for group in rank_groups.values():
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    self.graph.add_edge(group[i].card_name, group[j].card_name, type="set")

    def analyze_graph(self) -> Tuple[List[str], List[str]]:
        """
        Analyze the graph to determine the best sequences and sets.
        :return: A tuple containing lists of sequences and sets.
        """
        sequences = []
        sets = []

        for component in nx.connected_components(self.graph.to_undirected()):
            subgraph = self.graph.subgraph(component)
            edge_types = nx.get_edge_attributes(subgraph, "type")

            if all(t == "sequence" for t in edge_types.values()):
                sequences.append(list(component))
            elif all(t == "set" for t in edge_types.values()):
                sets.append(list(component))

        return sequences, sets
