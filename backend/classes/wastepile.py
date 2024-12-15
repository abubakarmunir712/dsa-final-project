from data_structures.stack import Stack


class WastePile:
    # Initialize pile with cards
    def __init__(self):
        self.pile = Stack()

    # Get top card
    def get_card(self):
        if self.pile.get_top() is None:
            return None
        if self.pile.get_top().is_joker():
            return None
        else:
            return self.pile.pop()
    
    # Get top card
    def get_top_card(self):
        if self.pile.get_top() is None:
            return None
        return self.pile.get_top()

    # Insert card
    def insert_card(self, card):
        self.pile.push(card)
        return True

    # If the waste pile is empty
    def is_empty(self):
        return self.pile.is_empty()