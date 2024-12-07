class Card:
    def __init__(self, suit, rank,color):
        self.suit = suit
        self.rank = rank
        self.color = color
        self.card_name = suit + "_" +rank
        self.visible = False
        self.joker = False

    def get_card_name(self):
        return self.card_name
    
    def get_suit(self):
        return self.suit
    
    def is_visible(self):
        return self.visible
    
    def is_joker(self):
        return self.isJoker
    
    def make_joker(self):
        self.isJoker = True

    def is_red(self):
        return self.color == "red"
    
    def is_black(self):
        return self.color == "black"
    
    def get_points(self):
        if self.rank =="A":
            return 20
        elif self.rank == "2":
            return 2
        elif self.rank == "3":
            return 3
        elif self.rank == "4":
            return 4
        elif self.rank == "5":
            return 5
        elif self.rank == "6":
            return 6
        elif self.rank == "7":
            return 7
        elif self.rank == "8":
            return 8
        elif self.rank == "9":
            return 9
        elif self.rank == "10":
            return 10
        elif self.rank == "J":
            return 10
        elif self.rank == "Q":
            return 10
        elif self.rank == "K":
            return 10
    
    def get_rank(self):
        if self.rank =="A":
            return 1
        elif self.rank == "2":
            return 2
        elif self.rank == "3":
            return 3
        elif self.rank == "4":
            return 4
        elif self.rank == "5":
            return 5
        elif self.rank == "6":
            return 6
        elif self.rank == "7":
            return 7
        elif self.rank == "8":
            return 8
        elif self.rank == "9":
            return 9
        elif self.rank == "10":
            return 10
        elif self.rank == "J":
            return 11
        elif self.rank == "Q":
            return 12
        elif self.rank == "K":
            return 13