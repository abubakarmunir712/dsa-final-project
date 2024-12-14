from game_logic.game import Game
from classes.player import Player
from classes.card import Card
from time import sleep
import os


def main():

    while True:
        os.system("clear")
        print("Welcome to Rummy Game")
        while True:
            no_of_players = int(input("Enter number of players (max. 6): "))
            if no_of_players > 6:
                print("Number of players cannot be more than 6")
            elif no_of_players == 1:
                print("You need atleast 2 players to play the game")
            else:
                break
        no_of_ai_players = 0
        if no_of_players < 6:
            while True:
                no_of_ai_players = int(
                    input(f"Enter number of players (max. {6-no_of_players}): ")
                )
                if no_of_ai_players > 6 - no_of_players:
                    print(
                        "Number of AI players cannot be more than the available slots"
                    )
                else:
                    break
        names = []
        for i in range(no_of_players - no_of_ai_players):
            name = input(f"Enter name of player {i+1}: ")
            names.append(name)
        game = Game(names, no_of_players, no_of_ai_players)
        player_turn = game.players_list.pop(0)
        turn_change = False
        is_card_drawn = False
        while True:
            os.system("cls")
            print(f"{game.joker} is the joker")
            print(f"""{player_turn.get_name()}'s turn""")
            print(player_turn.get_points())
            if turn_change:
                player_turn = game.players_list.pop(0)
                turn_change = False
            hand = player_turn.hand
            for i in range(5):
                print(f"Sequence {i+1}: {hand[i].get_sequence_status()}")
                for card in hand[i].get_cards():
                    print(card.card_name)
            player_move = user_choice(is_card_drawn)
            if player_move == "1" and not is_card_drawn:
                player_turn.get_card_from_stockpile(game.stockpile)
                is_card_drawn = True
            elif player_move == "2" and not is_card_drawn:
                if not game.wastepile.is_empty():
                    player_turn.get_card_from_wastepile(game.wastepile)
                else:
                    player_turn.get_card_from_stockpile(game.stockpile)
                is_card_drawn = True
            elif player_move == "3" and is_card_drawn:
                sequence_no = int(
                    input(
                        "Enter sequence number from where you want to discard the card: "
                    )
                )
                card_name = input("Enter card name to discard: ")
                player_turn.discard_card(sequence_no, card_name, game.wastepile)
                turn_change = True
                is_card_drawn = False
                sleep(2)
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
                player_turn.move_card(sequence_no_1 - 1, sequence_no_2 - 1, card_name)
            elif player_move == "5":
                cards_list = []
                while True:
                    sequence_no = int(input("Enter sequence number: "))
                    card_name = input("Enter card name: ")
                    cards_list.append((sequence_no-1, card_name))
                    if (
                        input("Do you want to add more cards to the group? (y/n): ")
                        == "n"
                    ):
                        break
                player_turn.group_cards(cards_list)
            if turn_change:
                game.players_list.append(player_turn)


def user_choice(is_card_drawn):
    if not is_card_drawn:
        print("1. Draw card from StockPile")
        print("2. Draw card from WastePile")
    else:
        print("3. Discard card")

    print("4. Move card from one sequence to another")
    print("5. Group cards")
    choice = input("Enter your choice: ")
    return choice


if __name__ == "__main__":
    main()
