from collections import deque
from typing import List

# Graph
class Graph:
    def _init_(self):
        self.adj_list = {}

    def add_node(self, state: str):
        if state not in self.adj_list:
            self.adj_list[state] = []

    def add_edge(self, state1: str, state2: str):
        self.adj_list[state1].append(state2)

    def bfs(self, start: str) -> List[str]:
        """Perform BFS on the graph."""
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                result.append(current)
                queue.extend(self.adj_list[current])

        return result

    def dfs(self, start: str) -> List[str]:
        """Perform DFS on the graph."""
        visited = set()
        stack = [start]
        result = []

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                result.append(current)
                stack.extend(self.adj_list[current])

        return result