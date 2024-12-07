class Card:

    def __init__(self, suit, rank,color):   #constructor 
        self.suit = suit
        self.rank = rank
        self.color = color
        self.CardName = suit + "_" +rank
        self.visible = False
        self.Joker = False


    #Basic functions for thecard Classs

    def getCardName(self):
        return self.CardName
    
    def getSuit(self):
        return self.suit
    
    def isVisible(self):
        return self.visible
    
    def isJoker(self):
        return self.isJoker
    
    def makeJoker(self):
        self.isJoker = True

    def isRed(self):
        return self.color == "red"
    
    def isBlack(self):
        return self.color == "black"
    
    def GetPoints(self):
        if self.rank =="A":
            return 10
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
    
    def getRank(self):
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