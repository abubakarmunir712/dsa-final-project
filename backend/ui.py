from game_logic.game import Game
import ui_utility
from time import sleep


# Main function
def main():
    # Main loop
    while True:
        # Main menu and header
        ui_utility.header()
        choice = ui_utility.main_menu()

        # Game play
        if choice == "1":

            ui_utility.header()

            # Input the number of players and AI players
            no_of_players, no_of_ai_players = ui_utility.game_players()
            
            # Creating a new game and initializing the player turn and card drawn for better turn management of player
            game = Game(no_of_players, no_of_ai_players)
            player_turn = game.players_list.pop(0)
            turn_change = False
            is_card_drawn = False
            
            # Game loop
            while True:
                ui_utility.header()
                # Printing the joker card
                print(f"{game.joker} is the joker")
                
                # Printing the player's turn and points
                print(f"""{player_turn.get_name()}'s turn""")
                print(player_turn.get_points())
                
                # Printing the player's hand
                ui_utility.print_cards(player_turn.get_hand())
                
                # Printing the stockpile and waste pile
                ui_utility.print_waste_and_stock_pile(game.wastepile,game.stockpile)

                if turn_change:
                    player_turn = game.players_list.pop(0)
                    turn_change = False
                
                player_move = ui_utility.player_choice(is_card_drawn)
                if player_move == "1" and not is_card_drawn:
                    player_turn.get_card_from_stockpile(game.stockpile)
                    print("Getting card from stock pile")
                    is_card_drawn = True
                elif player_move == "2" and not is_card_drawn:
                    if player_turn.get_card_from_wastepile(game.wastepile):
                        print("Card drawn from waste pile")
                    else:
                        player_turn.get_card_from_stockpile(game.stockpile)
                        print("Card drawn from stock pile")
                    sleep(1)
                    is_card_drawn = True
                elif player_move == "3" and is_card_drawn:
                    sequence_no = int(
                        input(
                            "Enter sequence number from where you want to discard the card: "
                        )
                    )
                    card_name = input("Enter card name to discard: ")
                    if player_turn.discard_card(
                        sequence_no - 1, card_name, game.wastepile
                    ):
                        print("Card discarded")
                        turn_change = True
                        is_card_drawn = False
                        sleep(2)
                    else:
                        print("Invalid card")
                        sleep(1)
                elif player_move == "4":
                    sequence_no_1 = int(
                        input(
                            "Enter sequence number from where you want to move the card: "
                        )
                    )
                    sequence_no_2 = int(
                        input("Enter sequence number where you want to move the card: ")
                    )
                    card_name = input("Enter card name: ")
                    player_turn.move_card(
                        sequence_no_1 - 1, sequence_no_2 - 1, card_name
                    )
                elif player_move == "5":
                    cards_list = []
                    while True:
                        sequence_no = int(input("Enter sequence number: "))
                        card_name = input("Enter card name: ")
                        cards_list.append((sequence_no - 1, card_name))
                        if (
                            input("Do you want to add more cards to the group? (y/n): ")
                            == "n"
                        ):
                            break
                    player_turn.group_cards(cards_list)
                if turn_change:
                    game.players_list.append(player_turn)
                if game.winner_selection():
                    print(f"{player_turn.get_name()} has won the game!")
                    ui_utility.print_cards(player_turn.hand)
                    break
        elif choice == "2":
            ui_utility.header()
            ui_utility.rules()
        elif choice == "3":
            break
        else:
            print("                     Invalid choice")
            sleep(1)


# Entry point of the program
if __name__ == "__main__":
    main()
