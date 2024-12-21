from collections import defaultdict
from time import sleep


class AIPlayer:
    def __init__(self, cards, name="AI", is_AI=True, player_id=None):
        self.name = name
        self.is_AI = is_AI
        self.graph = None
        self.current_hand = cards
        self.player_id = player_id

    def get_name(self):
        return self.name

    def build_graph(self):
        try:
            self.graph = defaultdict(list)
            for card in self.current_hand:
                rank, suit = card.get_rank(), card.suit
                # Add edges for sequences
                for next_card in self.current_hand:
                    next_rank, next_suit = next_card.get_rank(), next_card.suit
                    if suit == next_suit and next_rank == rank + 1:
                        self.graph[card].append(next_card)

                # Add edges for sets
                for same_rank_card in self.current_hand:
                    same_rank, same_suit = (
                        same_rank_card.get_rank(),
                        same_rank_card.suit,
                    )
                    if rank == same_rank and suit != same_suit:
                        self.graph[card].append(same_rank_card)
        except Exception as e:
            raise e

    def evaluate_hand(self):
        try:
            visited = set()
            sequences = []
            sets = []

            def dfs(card, path, is_run):
                visited.add(card)
                path.append(card)
                for neighbor in self.graph[card]:
                    if neighbor not in visited:
                        rank1, suit1 = card.get_rank(), card.suit
                        rank2, suit2 = neighbor.get_rank(), neighbor.suit
                        # Check for sequences
                        if is_run and suit1 == suit2 and rank2 == rank1 + 1:
                            dfs(neighbor, path, is_run)

                        # Check for sets
                        elif not is_run and rank1 == rank2 and suit1 != suit2:
                            dfs(neighbor, path, is_run)

            for card in self.current_hand:
                if card not in visited:
                    path = []
                    dfs(card, path, is_run=True)
                    if len(path) >= 3:  # Valid sequences
                        sequences.append(path)
                    path = []
                    dfs(card, path, is_run=False)
                    if len(path) >= 3:  # Valid sets
                        sets.append(path)

            return sequences, sets
        except Exception as e:
            raise e

    def get_points(self):
        try:
            self.build_graph()

            sequences, sets = self.evaluate_hand()
            matched_cards = set(card for seq in sequences for card in seq)
            matched_cards.update(set(card for s in sets for card in s))
            unmatched_cards = [
                card for card in self.current_hand if card not in matched_cards
            ]

            # Calculate points for unmatched cards
            points = 0
            for card in unmatched_cards:
                rank, suit = card.get_rank(), card.suit
                if rank in ["J", "Q", "K"]:
                    points += 10
                elif rank == "A":
                    points += 1
                elif rank == "Joker":
                    points += 0
                else:
                    points += rank
            return points
        except Exception as e:
            raise e

    def get_hand(self):
        return self.current_hand

    def choose_draw(self, stock_pile, waste_pile):
        try:
            if waste_pile.is_empty():  # If waste pile is empty, draw from stock pile
                return "stock"

            top_waste_card = (
                waste_pile.get_top_card()
            )  # Get the top card of the waste pile
            # Check if the waste pile is not empty and evaluate the hand with the waste card
            temp_hand = self.current_hand + [top_waste_card]
            self.build_graph()
            sequences, sets = self.evaluate_hand()
            if sequences or sets:
                return "waste"

            return "stock"
        except Exception as e:
            raise e

    def choose_discard(self):
        try:
            card_scores = {}
            for card in self.current_hand:
                temp_hand = [c for c in self.current_hand if c != card]
                self.current_hand = temp_hand
                self.build_graph()
                sequences, sets = self.evaluate_hand()
                score = len(sequences) + len(sets)
                card_scores[card] = score
                self.current_hand.append(card)

            # Find the card with the lowest score
            discard_card = min(card_scores, key=card_scores.get)
            self.current_hand.remove(discard_card)
            return discard_card
        except Exception as e:
            raise e

    def play(self, stock_pile, waste_pile):
        try:
            print(len(self.current_hand))
            # Build the graph for the current hand
            self.build_graph()

            # Draw a card from
            draw_choice = self.choose_draw(stock_pile, waste_pile)
            if draw_choice == "waste" and waste_pile:
                drawn_card = waste_pile.get_card()
            else:
                drawn_card = stock_pile.get_card()
            self.current_hand.append(drawn_card)

            # Evaluate the updated hand
            self.build_graph()
            sequences, sets = self.evaluate_hand()

            # Discard the least useful card
            discard_card = self.choose_discard()
            print(f"{self.name} discards: {discard_card.card_name}")
            waste_pile.insert_card(discard_card)
        except Exception as e:
            raise e
    
    def get_player_id(self):
        return self.player_id