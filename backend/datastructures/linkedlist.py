# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# LinkedList
class LinkedList:
    # Constructor
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # Insert at head
    def insert_at_head(self, data):

        # New node to be inserted
        new_node = Node(data)

        # If linkedlist is empty
        if self.head == None:
            self.head = new_node
            self.tail = new_node

        # If linkedlist is not empty
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def remove_from_head(self):

        temp = None

        # If linkedlist is empty
        if self.head == None:
            return None

        # If linkedlist is not empty

        # If head and tail are same
        if self.head == self.tail:
            temp = self.head
            self.head = None
            self.tail = None

        # If head's next element is tail
        elif self.head.next == self.tail:
            temp = self.head
            self.tail = self.head
            self.head.prev = None
            self.head.next = None

        # If head's next element is not tail
        else:
            temp = self.head
            self.head = self.head.next
            self.head.prev = None

        self.size -= 1
        return temp

    # Insert at tail
    def insert_at_tail(self, data):

        # New node to be inserted
        new_node = Node(data)

        # If linkedlist is empty
        if self.head == None:
            self.head = new_node
            self.tail = new_node

        # If linkedlist is not empty
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.size += 1

    # Remove from tail
    def remove_from_tail(self):
        temp = None

        # If linkedlist is empty
        if self.head == None:
            return None

        # If linkedlist is not empty

        # If head and tail are same
        if self.head == self.tail:
            temp = self.tail
            self.head = None
            self.tail = None

        # If head and tail are not same
        else:
            temp = self.tail
            self.tail = self.tail.prev
            self.tail.next = None

        self.size -= 1
        return temp

    # Viewing the first element
    def view_first_node(self):
        if self.head:
            return self.head
        else:
            return None

    # Viewing the last element  
    def view_last_node(self):
        if self.tail:
            return self.tail
        else:
            return None

    # Checks if the linkedlist is empty
    def is_empty(self):
        if self.head == None:
            return True
        else:
            return False

    # Get the size of the linkedlist
    def get_size(self):
        return self.size
    