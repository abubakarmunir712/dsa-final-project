class Graph:
    def __init__(self):
        self.graph = {}

    # Add an edge between two cards (i.e., they can form a valid sequence)
    def add_edge(self, card1, card2):
        if card1 not in self.graph:
            self.graph[card1] = []
        if card2 not in self.graph:
            self.graph[card2] = []
        self.graph[card1].append(card2)
        self.graph[card2].append(card1)

    # Get the neighbors of a card (i.e., cards that can form a valid sequence with it)
    def get_neighbors(self, card):
        return self.graph.get(card, [])

    # Check if there is an edge (valid sequence) between two cards
    def is_connected(self, card1, card2):
        return card2 in self.graph.get(card1, [])

    # Get all the cards that form sequences starting from the given card (DFS traversal)
    def get_sequence_from_card(self, card):
        visited = set()
        sequence = []
        self._dfs(card, visited, sequence)
        return sequence

    # Private helper method to perform DFS
    def _dfs(self, card, visited, sequence):
        stack = [card]
        while stack:
            current_card = stack.pop()
            if current_card not in visited:
                visited.add(current_card)
                sequence.append(current_card)
                for neighbor in self.get_neighbors(current_card):
                    if neighbor not in visited:
                        stack.append(neighbor)

    # Print the graph (for debugging purposes)
    def print_graph(self):
        for card, neighbors in self.graph.items():
            print(f"{card} -> {', '.join(str(neighbor) for neighbor in neighbors)}")
