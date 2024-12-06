from backend.datastructures.linklist import LinkedList

class Stack:
    
    def __init__(self):
        self.stack = LinkedList()

    def push(self, card):

        self.stack.insertAtHead(card)


    def pop(self):

        if self.stack.isEmpty():
            return -1
        
        top = self.stack.getFirstCard()
        self.stack.removeHead()

        return top

    def peek(self):

        if self.stack.isEmpty():
            return -1
        return self.stack.getFirstCard()

    def isEmpty(self):
        return self.stack.isEmpty()

    def size(self):
        return self.stack.size()
    
    