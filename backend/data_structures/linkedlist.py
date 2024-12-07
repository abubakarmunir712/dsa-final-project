# Node class
class Node:
    # Constructor
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


# LinkedList
class LinkedList:
    # Constructor
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__size = 0

    # Insert at head
    def insert_at_head(self, data):

        # New node to be inserted
        new_node = Node(data)

        # If linkedlist is empty
        if self.__head == None:
            self.__head = new_node
            self.__tail = new_node

        # If linkedlist is not empty
        else:
            new_node.next = self.__head
            self.__head.prev = new_node
            self.__head = new_node

        self.__size += 1

    def remove_from_head(self):

        temp = None

        # If linkedlist is empty
        if self.__head == None:
            return None

        # If linkedlist is not empty

        # If head and tail are same
        if self.__head == self.__tail:
            temp = self.__head
            self.__head = None
            self.__tail = None

        # If head's next element is tail
        elif self.__head.next == self.__tail:
            temp = self.__head
            self.__tail = self.__head
            self.__head.prev = None
            self.__head.next = None

        # If head's next element is not tail
        else:
            temp = self.__head
            self.__head = self.__head.next
            self.__head.prev = None

        self.__size -= 1
        return temp

    # Insert at tail
    def insert_at_tail(self, data):

        # New node to be inserted
        new_node = Node(data)

        # If linkedlist is empty
        if self.__head == None:
            self.__head = new_node
            self.__tail = new_node

        # If linkedlist is not empty
        else:
            self.__tail.next = new_node
            new_node.prev = self.__tail
            self.__tail = new_node

        self.__size += 1

    # Remove from tail
    def remove_from_tail(self):
        temp = None

        # If linkedlist is empty
        if self.__head == None:
            return None

        # If linkedlist is not empty

        # If head and tail are same
        if self.__head == self.__tail:
            temp = self.__tail
            self.__head = None
            self.__tail = None

        # If head and tail are not same
        else:
            temp = self.__tail
            self.__tail = self.__tail.prev
            self.__tail.next = None

        self.__size -= 1
        return temp

    # Viewing the first element
    def view_first_node(self):
        if self.__head:
            return self.__head
        else:
            return None

    # Viewing the last element
    def view_last_node(self):
        if self.__tail:
            return self.__tail
        else:
            return None

    # Checks if the linkedlist is empty
    def is_empty(self):
        if self.__head == None:
            return True
        else:
            return False

    # Get the size of the linkedlist
    def get_size(self):
        return self.__size
