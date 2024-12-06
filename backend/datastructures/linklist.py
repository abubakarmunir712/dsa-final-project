
class Node:
    def __init__(self, card):  #constructor
        self.card = card
        self.next = None

class LinkedList:

    def __init__(self):  #constructor
        self.head = None

    #linklist basic funstions

    def insertAtHead(self, card):

        node = Node(card)

        if self.head == None:
            self.head = node
            return
        else:      
            node.next = self.head
            self.head = node

    def insertAtTail(self, card):

        node = Node(card)

        if self.head == None:
            self.head = node
            return

        temp = self.head

        while temp.next:
            temp = temp.next

        temp.next = node

    def removeHead(self):
        
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

    def getFirstCard(self):

        if self.head:
            return self.head.card
        else:
            return None
        
    def getLastCard(self):
            
        if self.head:
            temp = self.head
            while temp.next:
                temp = temp.next
            return temp.card
        else:
            return None
        
    def isEmpty(self):
        if self.head == None:
            return True
        else:
            return False
