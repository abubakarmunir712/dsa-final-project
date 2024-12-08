# Hashmap
class HashMap:
    # Constructor
    def __init__(self, size):
        self.total_size = size  # Size of hashmap
        self.current_size = 0  # Total number of elements in hashmap
        self.map = [None] * size

    # Calculate hash using linear probing
    def _hash(self, key, i=0):
        return (hash(key) + i) % self.total_size

    # Resize hash table
    def resize(self, expand=True):
        self.temp_map = self.map  # Copy previous table
        self.current_size = 0

        if expand:
            self.total_size *= 2  # Double the size of hashmap
        else:
            self.total_size = max(1, self.total_size // 2)
        self.map = [None] * self.total_size  # Halve the size size of hasnmap

        for i in range(len(self.temp_map)):
            self.data = self.temp_map[i]
            if self.data is not None:
                self.insert(self.data[0], self.data[1])

    # Insert data in hashmap (Helper function for insert function)
    def _insert_data(self, key, value):
        for i in range(self.total_size):
            hash = self._hash(key, i)  # Calculate hash
            if self.map[hash] is None:
                self.map[hash] = (key, value)
                self.current_size += 1
                return (key, value)
            elif self.map[hash][0] == key:
                raise Exception("A value associated to this key already exists.")

    # Insert and resize hashmap
    def insert(self, key, value):
        if self.current_size <= self.total_size // 2:
            self._insert_data(key, value)
        else:
            self.resize()  # Expand Hashmap
            self._insert_data(key, value)

    # Get element associated with particular key
    def get(self, key):
        for i in range(self.total_size):
            data = self.map[self._hash(key, i)]
            if data is not None and data[0] == key:
                return data[1]

    # Remove and resize hashmap
    def remove(self, key):  # Remove element
        for i in range(self.total_size):
            self.index = self._hash(key, i)
            data = self.map[self.index]
            if data is not None and data[0] == key:
                self.map[self.index] = None
                self.current_size -= 1
                if self.current_size <= self.total_size // 5:
                    self.resize(False)  # Shrink hashmap
                return True
        return False
