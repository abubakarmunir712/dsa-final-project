import os


# Prints all the cards of the player in the hand
def print_cards(hand):
    for i in range(5):
        print(f"Sequence {i+1}: {hand[i].get_sequence_status()}")
        for card in hand[i].get_cards():
            print(card.card_name)


# Prints the header
def header():
    os.system("cls")
    print("Header\n\n")


# Player move choice
def player_choice(is_card_drawn):
    if not is_card_drawn:
        print("                     1. Draw card from StockPile")
        print("                     2. Draw card from WastePile")
    else:
        print("                     3. Discard card")

    print("                     4. Move card from one sequence to another")
    print("                     5. Group cards")
    choice = input("Enter your choice: ")
    return choice


# Main menu
def main_menu():
    print("                     1. Play a game")
    print("                     2. Rules")
    print("                     3. Exit")
    choice = input("Enter your choice: ")
    return choice


# Rules
def rules():
    print("                     Rules\n\n")
    print(
        """
            1. The game is played with two decks of cards with jokers.
            2. Each player is dealt 13 cards.
            3. The objective of the game is to form sequences and sets.
            4. A sequence is a group of three or more consecutive cards of the same suit.
            5. A set is a group of three or four cards of the same rank.
            6. A joker can be used as a substitute for any card.
            7. The game starts with a random card placed in the wastepile.
            8. The player can either draw a card from the stockpile or the wastepile.
            9. The player can discard a card to the wastepile.
            10. The player can move a card from one sequence to another.
            11. The player can group cards to form sequences or sets.
            12. The game ends when a player forms sequences and sets with all the cards in hand.
            13. The player with the least points wins the game.
            14. The points are calculated as the sum of the points of the cards not in any sequence or set.
            15. The points are calculated as follows:
                - Number cards have points equal to their face value.
                - Face cards have 10 points.
                - Jokers have 0 points.
            16. The winner of the game gets 0 points.
            17. The other players get points equal to the sum of the points of the cards in hand.
            18. The game can be played with 2 to 6 players."""
    )
    input("Press any key to continue...")


def game_players():
    print("                     Number of players\n\n")
    no_of_players = input("Enter number of total players(max. 6): ")
    if not no_of_players.isdigit():
        print("Number of players must be an integer")
    elif int(no_of_players) > 6:
        print("Number of players must be less than or equal to 6")
    elif int(no_of_players) < 2:
        print("Number of players must be greater than or equal to 2")
    else:
        no_of_players = int(no_of_players)
        no_of_ai_players = input(
            f"Enter number of AI players (max. {no_of_players-1}): "
        )
        if not no_of_ai_players.isdigit():
            print("Number of AI players must be an integer")
        elif int(no_of_ai_players) > no_of_players - 1:
            print(
                "Number of AI players must be at least 1 less than the total number of players"
            )
        else:
            no_of_ai_players = int(no_of_ai_players)
            if no_of_ai_players < 1:
                no_of_ai_players = 0
            return no_of_players, no_of_ai_players

    return 0, 0

# Printing the waste and stock pile
def print_waste_and_stock_pile(wastepile, stockpile):
    if wastepile.get_top_card():
            print(f"Wastepile top card:  {wastepile.get_top_card().card_name}")
    else:
        print("Waste pile is empty")
        
        
    if stockpile.get_top_card():
        print("Stockpile: Cards available in stock pile")