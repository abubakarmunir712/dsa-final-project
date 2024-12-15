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
            return ({"error": "Number of players and AI players must be an integer"},)
        if no_of_players <= no_of_ai_players:
            return {"error": "Atleast one player should not be AI"}
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
                return {"message": "Joined successfully!", "player-id": player_id}, 200
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
            cards = game.get_cards(player_id)
            if cards is None:
                return {"message": "Player not found"}, 404
            return {"cards": cards}
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
        result = game.remove_from_wastepile(player_id)

        if result == True:
            return {
                "message": "Card removed successfully",
                "cards": game.get_cards(),
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
        result = game.discard_card(player_id, sequence_no, card_name)
        if result == True:
            return {
                "message": "Message removed successfully",
                "cards": game.get_cards(player_id),
            }, 200
        elif result == False:
            return {"message": "Player not found"}, 404
        else:
            return {"message": result}, 400

    app.run(debug=True)


if __name__ == "__main__":
    main()
