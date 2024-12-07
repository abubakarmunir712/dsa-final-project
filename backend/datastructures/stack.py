from backend.datastructures.linklist import LinkedList

class Stack:
    
    def __init__(self):
        self.stack = LinkedList()


    def push(self, card):

        self.stack.insert_at_head(card)


    def pop(self):

        if self.stack.is_empty():
            return -1
        
        top = self.stack.view_first_node()
        self.stack.remove_from_head()

        return top

    def is_empty(self):
        return self.stack.is_empty()
    

    def get_size(self):
        return self.stack.size()
    

    def peek(self):

        if self.stack.is_empty():
            return -1
        return self.stack.view_first_node()


    