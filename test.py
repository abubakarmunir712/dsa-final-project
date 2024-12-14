import unittest
from backend.classes.card import Card
from backend.bot.bot import RummyBot
from backend.enums.status_enum import Status

class TestRummyBot(unittest.TestCase):

    def setUp(self):
        # Create mock player and cards
        class MockPlayer:
            def __init__(self):
                self.hand = []

            def get_hand(self):
                return self.hand

            def add_card_to_hand(self, card):
                self.hand.append(card)

            def remove_card_from_hand(self, card_name):
                self.hand = [card for card in self.hand if card.card_name != card_name]

        self.player = MockPlayer()
        self.bot = RummyBot(self.player)

        # Helper to create cards
        def create_card(rank, suit, is_joker=False):
            return Card(rank=rank, suit=suit, is_joker=is_joker)

        self.create_card = create_card

    def test_simple_sequence(self):
        # Add cards to player's hand
        self.player.hand = [
            self.create_card(2, "hearts"),
            self.create_card(3, "hearts"),
            self.create_card(4, "hearts"),
        ]
        self.assertTrue(self.bot.can_form_sequence(self.player.get_hand()))

    def test_simple_set(self):
        # Add cards to player's hand
        self.player.hand = [
            self.create_card(7, "spades"),
            self.create_card(7, "hearts"),
            self.create_card(7, "diamonds"),
        ]
        self.assertTrue(self.bot.can_form_set(self.player.get_hand()))

    def test_no_sequence_or_set(self):
        # Add cards to player's hand
        self.player.hand = [
            self.create_card(2, "hearts"),
            self.create_card(5, "clubs"),
            self.create_card(9, "diamonds"),
        ]
        self.assertFalse(self.bot.can_form_sequence(self.player.get_hand()))
        self.assertFalse(self.bot.can_form_set(self.player.get_hand()))

    def test_priority_to_sequence(self):
        # Add cards to player's hand
        self.player.hand = [
            self.create_card(2, "hearts"),
            self.create_card(3, "hearts"),
            self.create_card(4, "hearts"),
            self.create_card(7, "spades"),
            self.create_card(7, "hearts"),
            self.create_card(7, "diamonds"),
        ]
        # Build graph and analyze
        self.bot.build_graph(self.player.get_hand())
        sequences, sets = self.bot.analyze_graph()

        self.assertEqual(len(sequences), 1)
        self.assertEqual(len(sets), 1)

    def test_graph_with_joker(self):
        # Add cards to player's hand
        self.player.hand = [
            self.create_card(2, "hearts"),
            self.create_card(3, "hearts"),
            self.create_card(None, None, is_joker=True),  # Joker
        ]
        self.bot.build_graph(self.player.get_hand())
        sequences, sets = self.bot.analyze_graph()

        self.assertEqual(len(sequences), 1)  # Sequence should form with the joker

    def test_empty_discard_pile(self):
        # Add cards to player's hand
        self.player.hand = [
            self.create_card(5, "diamonds"),
            self.create_card(10, "clubs"),
        ]
        draw_pile = [self.create_card(2, "hearts"), self.create_card(7, "spades")]
        discard_pile = []  # Empty

        result = self.bot.play_turn(draw_pile, discard_pile)
        self.assertEqual(result, "TURN_COMPLETE")
        self.assertIn(draw_pile.pop(), self.player.get_hand())

if __name__ == "__main__":
    unittest.main()
