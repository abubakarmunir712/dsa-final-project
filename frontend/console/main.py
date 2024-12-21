from colorama import init, Fore
import os
import time
import requests
import socket
import psutil
import threading
import ipaddress

ip_list = []
server_ip = ""
game_id = ""
player_id = ""
is_game_started = False
is_my_turn = False
init()

# ------------------------------------Check IP------------------------------------------


# Get local ipv4 address
def get_my_local_ip():
    ip_list.clear()
    for interface_name, addresses in psutil.net_if_addrs().items():
        for addr in addresses:
            if addr.family == socket.AF_INET and addr.address != "127.0.0.1":
                ip_list.append((addr.address, addr.netmask, interface_name))


# Check if provided ip is valid
def is_ip_valid(ip):
    get_my_local_ip()
    for subnet_ip, subnet, interface_name in ip_list:
        try:
            network = ipaddress.IPv4Network(f"{subnet_ip}/{subnet}", strict=False)
            ip_obj = ipaddress.IPv4Address(ip)
            if ip_obj in network:
                return True
        except ValueError:
            continue
    return False


# ------------------------------------Functions for printing-------------------------------
# Generic function to print menus
def print_menu(
    statements_list,
    input_statement,
    error_statement,
    allowed_options,
    callback_functions=[],
):
    while True:
        for statement in statements_list:
            print(Fore.YELLOW + statement + Fore.RESET)
        option = input(input_statement)
        if option in allowed_options:
            return option
        else:
            clear_screen()
            for function in callback_functions:
                function()
            print(Fore.RED + error_statement + Fore.RESET)


# Print Game details
def print_game_details():
    clear_screen()
    print("Game ID: " + game_id)
    print(Fore.LIGHTMAGENTA_EX + "IP addresses: " + Fore.RESET)
    get_my_local_ip()
    for ip in ip_list:
        print(Fore.YELLOW + ip[2] + ": " + Fore.RESET + ip[0])
    # Print line
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    print("_" * columns)
    print()


# Print current game state
def print_current_state():
    get_cards_response = get_current_state()
    if get_cards_response is not None:
        cards = get_cards_response[0]
        joker = get_cards_response[1]
        stock_pile = get_cards_response[2]
        points = get_cards_response[3]
        global is_my_turn
        is_my_turn = get_cards_response[4]
        winner = get_cards_response[5]
        if winner != None:
            if winner == player_id:
                return "You have won the game!"
            else:
                return f"Player {winner} has won the game!"

        print(Fore.LIGHTMAGENTA_EX + "Joker card: " + Fore.RESET + joker)
        print(Fore.LIGHTMAGENTA_EX + "Waste pile: " + Fore.RESET + stock_pile)
        print(Fore.LIGHTMAGENTA_EX + "Points:     " + Fore.RESET + f"{points}")
        print(Fore.LIGHTMAGENTA_EX + "Your Turn:  " + Fore.RESET + f"{is_my_turn}")
        print()
        for index, group in enumerate(cards):
            print(Fore.GREEN + f"{index+1}->   ", end="" + Fore.RESET)
            for card_index, card in enumerate(group):
                if card_index == 0:
                    print(Fore.CYAN + pad_string(card, 22), end=" " + Fore.RESET)
                else:
                    if card[-1] == joker[-1]:
                        print(
                            Fore.LIGHTYELLOW_EX + pad_string(card, 13),
                            end=" " + Fore.RESET,
                        )
                    else:
                        print(pad_string(card, 13), end=" ")

            print("")
        print("")
        print("")
        return True
    return False


# ------------------------------------Helper functions---------------------------------------
# Clear screen
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# Add space to make string of desired length
def pad_string(string, length):
    if string is None:
        return "None"
    length_of_string = len(string)
    for i in range(length - length_of_string):
        string += " "
    return string


# -----------------------------------Getting data from server---------------------------------
# Get current state from server
def get_current_state():
    try:
        data = {"game-id": game_id, "player-id": player_id}
        respose = requests.get(server_ip + "get-cards", json=data)
        respose_data = respose.json()
        if respose.status_code == 200:
            global is_game_started
            is_game_started = True
            return (
                respose_data["cards"],
                respose_data["joker"],
                respose_data["stock-pile"],
                respose_data["points"],
                respose_data["is-my-turn"],
                respose_data["winner"],
            )
        else:
            print(Fore.RED + respose_data["message"] + Fore.RESET)
            return None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Error ocurred while connecting to server!" + Fore.RESET)


def group_cards(cards):
    data = {"game-id": game_id, "player-id": player_id, "cards": cards}
    try:
        response = requests.get(server_ip + "group-cards", json=data)
        response_data = response.json()
        if response.status_code == 200:
            return True
        else:
            return response_data["message"]
    except requests.exceptions.RequestException as e:
        print(e)


def move_cards(sequence_1, sequence_2, card_name):
    try:
        data = {
            "game-id": game_id,
            "player-id": player_id,
            "sequence-1": int(sequence_1) - 1,
            "sequence-2": int(sequence_2) - 1,
            "card-name": card_name,
        }
        try:
            response = requests.get(server_ip + "move-card", json=data)
            response_data = response.json()
            if response.status_code == 200:
                return True
            else:
                return response_data["message"]
        except requests.exceptions.RequestException as e:
            return "Request failed"
    except:
        return "Sequence numbers must be integer"


def get_from_waste_or_stock_pile(pile_name="stock"):
    data = {
        "game-id": game_id,
        "player-id": player_id,
    }
    try:
        response = requests.get(server_ip + f"get-from-{pile_name}-pile", json=data)
        response_data = response.json()
        if response.status_code == 200:
            return True
        else:
            return response_data["message"]
    except requests.exceptions.RequestException as e:
        return "Request failed"


def discard_card(sequence_no, card_name):
    try:
        data = {
            "game-id": game_id,
            "player-id": player_id,
            "sequence-no": int(sequence_no) - 1,
            "card-name": card_name,
        }
        try:
            response = requests.get(server_ip + f"discard-card", json=data)
            response_data = response.json()
            if response.status_code == 200:
                return True
            else:
                return response_data["message"]
        except requests.exceptions.RequestException as e:
            return "Request failed"
    except:
        return "Sequence numbers must be integer"


# ----------------------------------------Main functions----------------------------------------
# Main game loop
def play_game():
    print_game_details()
    while True:
        current_state_response = print_current_state()
        if current_state_response == True:
            game_menu_statements = [
                "1-> Refresh State",
                "2-> Group cards",
                "3-> Move card",
                "4-> Get from waste pile",
                "5-> Get from stock pile",
                "6-> Discard card",
            ]
            game_menu_input_statement = "\nEnter option: "
            game_menu_error_statement = "You have entered wrong option!"
            allowed_options = ["1", "2", "3", "4", "5", "6"]
            if not is_my_turn:
                del game_menu_statements[-3:]
                del allowed_options[-3:]
            option = print_menu(
                game_menu_statements,
                game_menu_input_statement,
                game_menu_error_statement,
                allowed_options,
                [print_game_details, print_current_state],
            )
            if option == "1":
                clear_screen()
                print_game_details()
                continue
            elif option == "2":
                try:
                    no_of_cards = int(
                        input(
                            Fore.LIGHTYELLOW_EX
                            + "Enter number of cards you want to group: "
                            + Fore.RESET
                        )
                    )
                    cards = []
                    for i in range(no_of_cards):
                        print(
                            Fore.LIGHTMAGENTA_EX
                            + f"Enter details for card no {i+1}"
                            + Fore.RESET
                        )
                        sequence_no = input(
                            Fore.YELLOW + "Enter sequence no: " + Fore.RESET
                        )
                        card_name = input(
                            Fore.YELLOW + "Enter card name: " + Fore.RESET
                        )
                        cards.append([int(sequence_no) - 1, card_name])
                    result = group_cards(cards)
                    clear_screen()
                    print_game_details()
                    if result != True:
                        print("Error: " + Fore.RED + result + Fore.RESET)
                        print("")

                except:
                    clear_screen()
                    print_game_details()

                    print(
                        "Error: "
                        + Fore.RED
                        + "No. of cards and sequence no. must be integer!"
                        + Fore.RESET
                    )
                    print("")
            elif option == "3":
                sequence_1 = input(
                    Fore.YELLOW
                    + "Enter sequence from where you want to move card: "
                    + Fore.RESET
                )
                sequence_2 = input(
                    Fore.YELLOW
                    + "Enter sequence to where you want to move card: "
                    + Fore.RESET
                )
                card_name = input(
                    Fore.YELLOW + "Enter name of card you want to move: " + Fore.RESET
                )
                result = move_cards(sequence_1, sequence_2, card_name)
                clear_screen()
                print_game_details()
                if result != True:
                    print("Error: " + Fore.RED + result + Fore.RESET)
                    print("")

            elif option == "4":
                result = get_from_waste_or_stock_pile("waste")
                clear_screen()
                print_game_details()
                if result != True:
                    print("Error: " + Fore.RED + result + Fore.RESET)
                    print("")
            elif option == "5":
                result = get_from_waste_or_stock_pile("stock")
                clear_screen()
                print_game_details()
                if result != True:
                    print("Error: " + Fore.RED + result + Fore.RESET)
                    print("")
            elif option == "6":
                sequence_no = input(
                    Fore.YELLOW
                    + "Enter sequence from where you want to discard card: "
                    + Fore.RESET
                )
                card_name = input(
                    Fore.YELLOW
                    + "Enter the name of card to be discarded: "
                    + Fore.RESET
                )
                result = discard_card(sequence_no, card_name)
                clear_screen()
                print_game_details()
                if result != True:
                    print("Error: " + Fore.RED + result + Fore.RESET)
                    print("")
        elif current_state_response == False:
            time.sleep(3)
        else:
            clear_screen()
            print(current_state_response)
            break


def main():
    clear_screen()
    while True:
        # Print main menu
        main_menu_statements = ["1-> Create Game", "2-> Join Game", "3-> Exit"]
        main_menu_input_statement = "Enter option: "
        main_menu_error_statement = "You have entered wrong option! Please try again"
        allowed_options = ["1", "2", "3"]
        option = print_menu(
            main_menu_statements,
            main_menu_input_statement,
            main_menu_error_statement,
            allowed_options,
        )
        clear_screen()
        if option == "1":
            global server_ip
            try:
                # Check if server is running
                response = requests.get("http://127.0.0.1:5000/connect")
                if response.status_code == 200:
                    server_ip = "http://127.0.0.1:5000/"
                    clear_screen()

                    # Get input for number of players and ai players
                    no_of_players = input(
                        Fore.LIGHTMAGENTA_EX + "Enter number of players: " + Fore.RESET
                    )
                    no_of_ai_players = input(
                        Fore.LIGHTMAGENTA_EX
                        + "Enter number of AI players: "
                        + Fore.RESET
                    )
                    clear_screen()

                    # Create Game
                    response = requests.get(
                        server_ip
                        + f"create-game?players={no_of_players}&ai_players={no_of_ai_players}"
                    )

                    data = response.json()
                    if response.status_code == 200:
                        global game_id
                        global player_id

                        game_id = data["game-id"]
                        # Join game if game is created successfully
                        response = requests.get(server_ip + "join-game/" + game_id)
                        data = response.json()

                        if response.status_code == 200:
                            player_id = data["player-id"]
                            print(Fore.GREEN + "Game created successfully" + Fore.RESET)
                            input(
                                Fore.LIGHTMAGENTA_EX
                                + "Press Enter to continue ...."
                                + Fore.RESET
                            )
                            play_game()
                        else:
                            data = response.json()
                            print(Fore.RED + data["message"] + Fore.RESET)
                    else:
                        print(Fore.RED + data["message"] + Fore.RESET)

            except requests.exceptions.RequestException as e:
                print(
                    Fore.RED + "Error ocurred while connecting to server!" + Fore.RESET
                )
        elif option == "2":
            server_ip = input("Enter server ip: ")
            if not is_ip_valid(server_ip):
                clear_screen()
                print(
                    "Error: "
                    + Fore.RED
                    + "Server ip is not valid or you are not connected to network"
                    + Fore.RESET
                )
                continue
            server_ip = f"http://{server_ip}:5000/"

            game_id = input("Enter game Id: ")
            try:
                response = requests.get(server_ip + f"join-game/{game_id}")
                response_data = response.json()
                if response.status_code == 200:
                    player_id = response_data["player-id"]
                    play_game()
                else:
                    clear_screen()
                    game_id = ""
                    server_ip = ""
                    print("Error: " + Fore.RED + data["message"] + Fore.RESET)
            except requests.exceptions.RequestException as e:
                print(e)
                print("Error: " + Fore.RED + "Request failed" + Fore.RESET)
        else:
            clear_screen()
            exit()


if __name__ == "__main__":
    main()
