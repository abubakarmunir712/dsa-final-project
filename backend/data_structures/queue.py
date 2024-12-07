from data_structures.linkedlist import LinkedList


# Queue
class Queue:
    # Constructor
    def __init__(self):
        self.__queue = LinkedList()

    # Enqueue element
    def enqueue(self, data):
        self.__queue.insert_at_tail(data)

    # Dequeue element
    def dequeue(self):
        return self.__queue.remove_from_head()

    # Get size of the queue
    def get_size(self):
        return self.__queue.get_size()

    # Getting the first card, the head of queue
    def get_first_element(self):
        return self.__queue.view_first_node()

    # Check if the queue is empty
    def is_empty(self):
        return self.__queue.is_empty()
