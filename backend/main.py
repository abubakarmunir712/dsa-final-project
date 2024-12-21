from game_logic.game import Game
from flask import Flask, request
from data_structures.hashmap import HashMap


def main():

    games = {}
    app = Flask(__name__)

    # -----------------------------------------------------------------------------------
    # Create a new game
    @app.route("/create-game")
    def create_game():
        try:
            no_of_players = int(request.args.get("players"))
            no_of_ai_players = int(request.args.get("ai_players"))
        except:
            return {
                "message": "Number of players and AI players must be an integer"
            }, 400
        if no_of_players <= no_of_ai_players:
            return {"message": "Atleast one player should not be AI"}, 400
        game = Game([], no_of_players, no_of_ai_players)
        print(game.players_joined)
        print(game.no_of_players)
        games[game.game_id] = game
        return {"message": "Game created successfully!", "game-id": game.game_id}, 200

    # -----------------------------------------------------------------------------------
    # Join a game
    # endpoint = "/join-game/game_id_here"

    @app.route("/join-game/<game_id>")
    def join_game(game_id):
        if game_id in games:
            game: Game = games[game_id]
            if game.players_joined < game.no_of_players:
                player_id = game.players_list[game.players_joined].player_id
                game.players_joined += 1
                if game.players_joined == game.no_of_players:
                    game.is_started = True
                return {
                    "message": "Joined successfully!",
                    "player-id": player_id,
                    "isAi": game.players_list[game.players_joined - 1].is_AI,
                }, 200
            else:
                return {"message": "Room is full", "players": game.no_of_players}, 403
        else:
            return {"message": "Room not found"}, 404

    # -----------------------------------------------------------------------------------
    # Get player cards
    # endpoint = "/join-game"
    # requires body in this form {"game-id":"game id here", "player-id":"player id here"}

    @app.route("/get-cards")
    def get_cards():

        data = request.get_json()
        if not data:
            return {"message": "Game id and Player id is required"}, 400
        game_id = data.get("game-id")
        player_id = data.get("player-id")
        # Game id and player id must be present
        if game_id is None or player_id is None:
            return {"message": "Both game id and player id are required"}, 400

        if game_id in games:
            game: Game = games[game_id]
            if not game.is_started:
                return {"message": "Game is not started yet"}, 400
            cards = game.get_cards(player_id)
            if cards is None:
                return {"message": "Player not found"}, 404
            if game.players_list[game.current_player].player_id == player_id:
                _is_my_turn = True
            else:
                _is_my_turn = False
            return {
                "joker": game.joker_card,
                "points": game.get_player(player_id).get_points(),
                "cards": cards,
                "stock-pile": (
                    "Empty"
                    if game.wastepile.is_empty()
                    else game.wastepile.get_top_card().card_name
                ),
                "is-my-turn": _is_my_turn,
                "winner": (
                    game.winner_selection()
                    if game.winner_selection() is None
                    else game.winner_selection().player_id
                ),
            }
        else:
            return {"message": "Game not found!"}, 404

    # -----------------------------------------------------------------------------------
    # Get card from wastepile
    # endpoint = "/get-from-waste-pile"
    # requires body in this form {"game-id":"game id here", "player-id":"player id here"}

    @app.route("/get-from-waste-pile")
    def get_from_waste_pile():
        data = request.get_json()
        if not data:
            return {"message": "Game id and Player id is required"}, 400
        game_id = data.get("game-id")
        player_id = data.get("player-id")

        # Game id and player id must be present
        if game_id is None or player_id is None:
            return {"message": "Both game id and player id are required"}, 400
        if game_id not in games:
            return {"message": "Game not found"}, 404

        game: Game = games[game_id]
        if not game.is_started:
            return {"message": "Game is not started yet"}, 400
        if game.players_list[game.current_player].player_id != player_id:
            return {"message": "It's not your turn"}, 400

        result = game.remove_from_wastepile(player_id)

        if result == True:
            return {
                "message": "Card removed successfully",
                "cards": game.get_cards(player_id),
            }, 200
        elif result == False:
            return {"message": "Player not found"}, 404
        else:
            return {"message": result}, 400

    # -----------------------------------------------------------------------------------
    # Get card from stockpile
    # endpoint = "/get-from-stock-pile"
    # requires body in this form {"game-id":"game id here", "player-id":"player id here"}

    @app.route("/get-from-stock-pile")
    def remove_from_stock_pile():
        data = request.get_json()
        if not data:
            return {"message": "Game id and Player id is required"}, 400
        game_id = data.get("game-id")
        player_id = data.get("player-id")

        # Game id and player id must be present
        if game_id is None or player_id is None:
            return {"message": "Both game id and player id are required"}, 400
        if game_id not in games:
            return {"message": "Game not found"}, 404

        game: Game = games[game_id]
        if not game.is_started:
            return {"message": "Game is not started yet"}, 400
        if game.players_list[game.current_player].player_id != player_id:
            return {"message": "It's not your turn"}, 400
        result = game.remove_from_stockpile(player_id)

        if result == True:
            return {
                "message": "Card removed successfully",
                "cards": game.get_cards(player_id),
            }, 200
        elif result == False:
            return {"message": "Player not found"}, 404
        else:
            return {"message": result}, 400

    # -----------------------------------------------------------------------------------
    # Get card from stockpile
    # endpoint = "/discard-card"
    """requires body in this form
    {
    "game-id":"game id here",
    "player-id":"player id here",
    "sequence-no":"sequence no here",
    "card-name":"card name here"
    }
    """

    @app.route("/discard-card")
    def discard_Card():
        data = request.get_json()
        if not data:
            return {"message": "Game id and Player id is required"}, 400
        game_id = data.get("game-id")
        player_id = data.get("player-id")
        sequence_no = data.get("sequence-no")
        card_name = data.get("card-name")
        if sequence_no is None or card_name is None:
            return {"message": "Both sequence and card_name are required"}, 400
        # Game id and player id must be present
        if game_id is None or player_id is None:
            return {"message": "Both game id and player id are required"}, 400
        if game_id not in games:
            return {"message": "Game not found"}, 404
        game: Game = games[game_id]
        if not game.is_started:
            return {"message": "Game is not started yet"}, 400
        if game.players_list[game.current_player].player_id != player_id:
            return {"message": "It's not your turn"}, 400
        result = game.discard_card(player_id, sequence_no, card_name)
        if result == True:
            print(game.move_to_next_player())
            return {
                "message": "Message removed successfully",
                "cards": game.get_cards(player_id),
            }, 200
        elif result == False:
            return {"message": "Player not found"}, 404
        else:
            return {"message": result}, 400

    # -----------------------------------------------------------------------------------
    # Get card from stockpile
    # endpoint = "/move-card"
    """requires body in this form
    {
    "game-id":"game id here",
    "player-id":"player id here",
    "sequence-1":"sequence no 1 here",
    "sequence-2":"sequence no 2 here",
    "card-name":"card name here"
    }
    """

    @app.route("/move-card")
    def move_card():
        data = request.get_json()
        if not data:
            return {"message": "Game id and Player id is required"}, 400
        game_id = data.get("game-id")
        player_id = data.get("player-id")
        sequence_no_1 = data.get("sequence-1")
        sequence_no_2 = data.get("sequence-2")
        card_name = data.get("card-name")
        if sequence_no_1 is None or card_name is None or sequence_no_2 is None:
            return {"message": "Both sequences and card_name are required"}, 400
        # Game id and player id must be present
        if game_id is None or player_id is None:
            return {"message": "Both game id and player id are required"}, 400
        if game_id not in games:
            return {"message": "Game not found"}, 404
        game: Game = games[game_id]
        if not game.is_started:
            return {"message": "Game is not started yet"}, 400
        result = game.move_cards(player_id, sequence_no_1, sequence_no_2, card_name)
        if result == True:
            return {
                "message": "Moved successfully",
                "cards": game.get_cards(player_id),
            }, 200
        elif result == None:
            return {"message": "Player not found"}, 404
        else:
            return {"message": result}, 400

    # -----------------------------------------------------------------------------------
    # Group cards
    # endpoint = "/group-cards"
    """requires body in this form
    {
    "game-id":"game id here",
    "player-id":"player id here",
    "cards":[[seq_no,"card_name"],[seq_no,"card_name"]]
    }
    """

    @app.route("/group-cards")
    def group_cards():
        data = request.get_json()
        if not data:
            return {"message": "Game id and Player id is required"}, 400
        game_id = data.get("game-id")
        player_id = data.get("player-id")
        cards = data.get("cards")
        cards = [tuple(card) for card in cards]
        if cards is None:
            return {"message": "Cards are required"}, 400
        # Game id and player id must be present
        if game_id is None or player_id is None:
            return {"message": "Both game id and player id are required"}, 400
        if game_id not in games:
            return {"message": "Game not found"}, 404
        game: Game = games[game_id]
        if not game.is_started:
            return {"message": "Game is not started yet"}, 400
        result = game.make_group(player_id, cards)
        if result == True:
            return {
                "message": "Made group successfully",
            }, 200
        elif result == False:
            return {"message": "Player not found"}, 404
        else:
            return {"message": result}, 400

    @app.route("/connect")
    def connect():
        return {"message": "Server is running"}, 200

    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
