from datastructures.linkedlist import LinkedList

class Queue:
    
    def __init__(self):
        self.queue = LinkedList()


    def enqueue(self, card):
        self.queue.insert_at_tail(card)

    def dequeue(self):
        if self.queue.is_empty():
            return -1
        
        front = self.queue.view_first_node()

        self.queue.remove_from_head()
        return front

    def peek(self):
        if self.queue.is_empty():
            return -1
        return self.queue.view_first_node()


    def is_empty(self):
        return self.queue.is_empty()


    def get_size(self):
        return self.queue.size()
