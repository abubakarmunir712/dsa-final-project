from game_logic.game import Game
import ui_utility
from time import sleep
from classes.card import Card
from classes.player import Player

from enums.rank_enum import Rank
from enums.suit_enum import Suit
# Main function
def main():
    # Main loop
    while True:
        # Main menu and header
        ui_utility.header()
        choice = ui_utility.main_menu()

        # Game play
        if choice == "1":

            try:
                ui_utility.header()

                # Input the number of players and AI players
                no_of_players, no_of_ai_players = ui_utility.game_players()

                print(no_of_players, no_of_ai_players)

                # Creating a new game and initializing the player turn and card drawn for better turn management of player
                game = Game(None,no_of_players, no_of_ai_players)
                turn_change = False
                is_card_drawn = False


                # Initialize the player hand with Card objects
                player_hand = [
                    Card(Suit.DIAMONDS.value, Rank.FIVE.value),
                    Card(Suit.DIAMONDS.value, Rank.SIX.value),
                    Card(Suit.DIAMONDS.value, Rank.SEVEN.value),
                    Card(Suit.DIAMONDS.value, Rank.EIGHT.value),
                    Card(Suit.DIAMONDS.value, Rank.NINE.value),
                    Card(Suit.DIAMONDS.value, Rank.TEN.value),
                    Card(Suit.CLUBS.value, Rank.THREE.value),
                    Card(Suit.DIAMONDS.value, Rank.THREE.value),
                    Card(Suit.HEARTS.value, Rank.THREE.value),
                    Card(Suit.SPADES.value, Rank.NINE.value),
                    Card(Suit.HEARTS.value, Rank.NINE.value),
                    Card(Suit.CLUBS.value, Rank.NINE.value),
                    Card(None, None, is_joker=True),  # Joker card
                ]

                player = Player(player_hand, "Player 1",False)
                game.players_list.append(player)
                player_turn = game.get_players_list().pop(0)

                # Game loop
                while True:
                    ui_utility.header()
                    
                    # Player's turn management
                    if turn_change:
                        game.players_list.append(player_turn)
                        player_turn = game.players_list.pop(0)
                        turn_change = False
                        is_card_drawn = False
                    
                    # Printing the joker card
                    print(f"{game.get_wild_joker()} is the joker")

                    # Printing the player's turn and points
                    print(f"""{player_turn.get_name()}'s turn""")
                    print(player_turn.get_points())

                    # Printing the player's hand
                    ui_utility.print_cards(player_turn.get_hand())

                    # Printing the stockpile and waste pile
                    ui_utility.print_waste_and_stock_pile(game.wastepile, game.stockpile)


                    # AI player's turn
                    if player_turn.is_AI:
                        player_turn.play()
                        turn_change = True
                        is_card_drawn = False
                        sleep(2)
                        continue

                    # Human Player's turn

                    # Player's choice
                    player_move = ui_utility.player_choice(is_card_drawn)

                    # Player's move
                    
                    # Draw card from stockpile
                    if player_move == "1" and not is_card_drawn:
                        player_turn.get_card_from_stockpile(game.stockpile)
                        ui_utility.print_statement("Getting card from stock pile")
                        is_card_drawn = True

                    # Draw card from waste pile
                    elif player_move == "2" and not is_card_drawn:
                        if player_turn.get_card_from_wastepile(game.wastepile):
                            ui_utility.print_statement("Card drawn from waste pile")
                        else:
                            player_turn.get_card_from_stockpile(game.stockpile)
                            ui_utility.print_statement("Card drawn from stock pile")
                        sleep(1)
                        is_card_drawn = True

                    # Discard card
                    elif player_move == "3" and is_card_drawn:
                        sequence_no,card_name = ui_utility.discard_card_input()
                        if sequence_no_1 and card_name:
                            if player_turn.discard_card(
                                sequence_no - 1, card_name, game.wastepile
                            ):
                                ui_utility.print_statement("Card discarded")
                                turn_change = True
                                is_card_drawn = False
                                sleep(2)
                            else:
                                ui_utility.print_statement("Invalid card")
                                sleep(1)
                        else:
                            ui_utility.print_statement("Invalid card")
                            sleep(1)

                    # Move card from one sequence to another
                    elif player_move == "4":
                        sequence_no_1, sequence_no_2, card_name = ui_utility.move_card_input()
                        if sequence_no_1 and sequence_no_2 and card_name:
                            if player_turn.move_card(
                                sequence_no_1 - 1, sequence_no_2 - 1, card_name
                            ):
                                ui_utility.print_statement("Card moved")
                            else:
                                ui_utility.print_statement("Invalid move")
                            sleep(1)


                    # Group cards
                    elif player_move == "5":
                        cards_list = []
                        while True:
                            sequence_no,card_name = ui_utility.discard_card_input()
                            if(sequence_no and card_name):
                                cards_list.append((sequence_no - 1, card_name))
                                if (
                                    input(
                                        "                     Do you want to add more cards to the group? (y/n): "
                                    ).lower()
                                    == "n"
                                ):
                                    break
                        if player_turn.group_cards(cards_list):
                            ui_utility.print_statement("Cards grouped")

                    # Invalid choice
                    else:
                        ui_utility.print_statement("Invalid choice")
                        sleep(1)

                    # Check if the player has won
                    if game.winner_selection():
                        ui_utility.print_statement(
                            f"{player_turn.get_name()} has won the game!"
                        )
                        ui_utility.print_cards(player_turn.get_hand())
                        sleep(10)
                        break

            except Exception as e:
                ui_utility.print_statement(f"An error occurred: {e}")
                sleep(1)

        # Rules
        elif choice == "2":
            ui_utility.header()
            ui_utility.rules()

        # Exit
        elif choice == "3":
            break

        # Invalid choice
        else:
            ui_utility.print_statement("Invalid choice")
            sleep(1)


# Entry point of the program
if __name__ == "__main__":
    main()
