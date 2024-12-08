from classes.sequence import Sequence


# Player
class Player:
    # Constructor
    def __init__(self, name, is_AI=False, game_id=None):
        self.__hand = [Sequence() * 5]
        self.__name = name
        self.__points = 0
        self.__is_AI = is_AI
        self.__game_id = game_id

    # Getters for attributes
    def get_name(self):
        return self.__name

    def get_hand(self):
        return self.__hand

    def get_points(self):
        return self.__points

    def get_is_AI(self):
        return self.__is_AI

    def get_game_id(self):
        return self.__game_id
