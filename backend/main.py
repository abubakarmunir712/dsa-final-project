from game_logic.game import Game
from flask import Flask, request
from data_structures.hashmap import HashMap


def main():

    games = {}
    app = Flask(__name__)

    # Create a new game
    @app.route("/create-game")
    def create_game():
        try:
            no_of_players = int(request.args.get("players"))
            no_of_ai_players = int(request.args.get("ai_players"))
        except:
            return {"error": "Number of players and AI players must be an integer"}, 400

        game = Game(no_of_players, no_of_ai_players)
        games[game.game_id] = game
        return {"message": "Game created successfully!", "game-id": game.game_id}, 200

    # Join a game
    @app.route("/join-game/<game_id>")
    def join_game(game_id):
        if game_id in games:
            game: Game = games[game_id]
            if game.players_joined < game.no_of_players:
                player_id = game.players_list[game.players_joined].player_id
                game.players_joined += 1
                return {"message": "Joined successfully!", "player-id": player_id}, 200
            else:
                return {"message": "Room is full"}, 403
        else:
            return {"message": "Room not found"}, 404
    @app.route("get-cards/<game_id>/<player_id>")
    def get_cards(game_id,player_id):
        pass

    app.run(debug=True)


if __name__ == "__main__":
    main()
