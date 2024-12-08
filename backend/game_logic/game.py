import uuid
class Game:
    def __init__(self,no_of_players=2, no_ai_players=0):
        self.game_id = str(uuid.uuid4())
