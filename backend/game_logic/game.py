from classes.deck import Deck
from classes.player import Player
from bot.bot import AIPlayer
from classes.stockpile import StockPile
from classes.wastepile import WastePile
from typing import List
import uuid


class Game:
    def __init__(self, player_names=None, no_of_players=2, no_of_ai_players=0):
        self.game_id = str(uuid.uuid4())
        self.no_of_players = no_of_players
        self.players_list: List[Player] = []
        self.players_joined = no_of_ai_players
        self.cards = Deck()
        self.joker = self.cards.joker  # Printed joker in this game
        # Create players
        for i in range(no_of_players):
            is_AI = True if i < no_of_ai_players else False
            player_cards = []
            player_id = str(uuid.uuid4())

            # Getting cards for player
            for j in range(13):
                player_cards.append(self.cards.draw_card())

            if is_AI:
                self.players_list.append(
                    AIPlayer(player_cards, f"AI Player {i}", is_AI, player_id)
                )
            else:
                self.players_list.append(
                    Player(player_cards, "Unknown", is_AI, player_id)
                )
            

        self.stockpile = StockPile(self.cards.get_all_cards())
        del self.cards  # Delete deck object
        self.wastepile = WastePile()

    # Get cards of a player by player id
    def get_cards(self, player_id):
        for player in self.players_list:
            if player.get_player_id() == player_id:
                cards_list = []
                for sequence in player.get_hand():
                    sequence_status = sequence.get_sequence_status()
                    card_names = [card.card_name for card in sequence.get_cards()]
                    cards_list.append([sequence_status] + card_names)
                return cards_list

        return None

    # Move cards of player from one sequence to other
    def move_cards(self, player_id, sequence_no_1, sequence_no_2, card_name):
        for player in self.players_list:
            if player.get_player_id() == player_id:
                return player.move_card(sequence_no_1, sequence_no_2, card_name)
        return None

    # Group cards
    def make_group(self, player_id, cards_list):
        if self.is_valid_card_list(cards_list):
            for player in self.players_list:
                if player.get_player_id() == player_id:
                    return player.group_cards(cards_list)
        return False

    def is_valid_card_list(input_data):
        # Check if input_data is a list
        if not isinstance(input_data, list):
            return False

        # Check each element in the list
        for item in input_data:
            # Ensure each item is a tuple and has exactly two elements
            if not isinstance(item, tuple) or len(item) != 2:
                return False

            # Ensure the first element is an integer and the second is a string
            if not isinstance(item[0], int) or not isinstance(item[1], str):
                return False

        return True

    # Get card from stock pile
    def remove_from_stockpile(self, player_id):
        for player in self.players_list:
            if player.get_player_id() == player_id:
                return player.get_card_from_stockpile(self.stockpile)
        return False

    # Get card from waste pile
    def remove_from_wastepile(self, player_id):
        for player in self.players_list:
            if player.get_player_id() == player_id:
                return player.get_card_from_wastepile(self.wastepile)
        return False

    # Discard card or move to waste pile
    def discard_card(self, player_id, sequence_no, card_name):
        for player in self.players_list:
            if player.get_player_id() == player_id:
                return player.discard_card(sequence_no, card_name, self.wastepile)
        return False

    # Winner selection
    def winner_selection(self):
        # Check if any player has 0 points to win the game
        for player in self.players_list:
            if player.get_points() == 0:
                return player

        # Check if stockpile and wastepile are empty then lowest points player wins the game
        if self.stockpile.is_empty() and (
            self.wastepile.is_empty() or self.wastepile.get_top_card().is_joker()
        ):
            min_points = 999
            winner = None
            # Finding player with lowest points
            for player in self.players_list:
                if player.get_points() < min_points:
                    min_points = player.get_points()
                    winner = player
            return winner

        return None
