from backend.datastructures.linklist import LinkedList


class Queue:
    
    def __init__(self):
        self.queue = LinkedList()

    def enqueue(self, card):
        self.queue.insertAtTail(card)

    def dequeue(self):
        if self.queue.isEmpty():
            return -1
        
        front = self.queue.getFirstCard()
        self.queue.removeHead()
        return front

    def peek(self):
        if self.queue.isEmpty():
            return -1
        return self.queue.getFirstCard()

    def isEmpty(self):
        return self.queue.isEmpty()

    def size(self):
        return self.queue.size()