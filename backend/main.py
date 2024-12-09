from game_logic.game import Game
from classes.player import Player
from classes.card import Card

a = [
    Card("hearts", "A"),
    Card("hearts", "Q",True),
    Card("hearts", "K"),
    Card("spades", "2"),
    Card("clubs", "4"),
    Card("spades", "3"),
    Card("spades", "4"),
    Card("hearts", "J"),
]

p = Player(a)
