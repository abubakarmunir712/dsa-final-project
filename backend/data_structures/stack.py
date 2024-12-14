from data_structures.linkedlist import LinkedList


# Stack
class Stack:
    # Constructor
    def __init__(self):
        self.__stack = LinkedList()

    # Push element
    def push(self, data):
        self.__stack.insert_at_head(data)

    # pop element
    def pop(self):
        return self.__stack.remove_from_head().data

    # Get size of the stack
    def get_size(self):
        return self.__stack.get_size()

    # Getting the first card, the head of stack
    def get_top(self):
        return self.__stack.view_first_node().data

    # Check if the queue is empty
    def is_empty(self):
        return self.__stack.is_empty()
