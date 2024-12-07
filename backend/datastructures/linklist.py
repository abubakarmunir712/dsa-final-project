class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, data):
        node = Node(data)

        if self.head == None:
            self.head = node
            return
        else:
            node.next = self.head
            self.head = node

    def insert_at_tail(self, data):

        node = Node(data)

        if self.head == None:
            self.head = node
            return

        temp = self.head

        while temp.next:
            temp = temp.next

        temp.next = node

    def remove_from_head(self):
        
        if self.head == None:
            return

        self.head = self.head.next

    def removeTail(self):

        if self.head:
            temp = self.head
            # while temp.next:
            while temp:
                temp = temp.next
            temp = None
            if self.head.next is None:
                self.head = None
            else:
                temp = self.head
                while temp.next.next:
                    temp = temp.next
                temp.next = None
        else:
            return None

    def size(self):

        size = 0
        if self.head:
            temp = self.head
            while temp:
                size += 1
                temp = temp.next
            return size
        else:
            return 0

    def view_first_node(self):

        if self.head:
            return self.head.data
        else:
            return None
        
    def view_last_node(self):
            
        if self.head:
            temp = self.head
            while temp.next:
                temp = temp.next
            return temp.data
        else:
            return None
        
    def is_empty(self):
        if self.head == None:
            return True
        else:
            return False
        
    def get_at_index(self, index):
        if self.head:
            temp = self.head
            for i in range(index):
                if temp.next:
                    temp = temp.next
                else:
                    return None
            return temp.data
        else:
            return None