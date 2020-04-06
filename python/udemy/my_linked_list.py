class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, data):
        new_node = Node(data)

        # If linked list is empty
        if self.head == None:
            self.head = new_node
            self.tail = new_node
            self.length = 1
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.length += 1

    def prepend(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head == new_node
            self.tail -- new_node
            self.length = 1
        else:
            new_node.next = self.head
            self.head = new_node

    def insert(self, index, data):
        if index >= self.length:
            self.append(data)
        elif index == 0:
            self.prepend(data)
        while ()
            new_node = Node(data)
            cur_index = 0
            cur_node = self.head
            while cur_index != index:
                cur_node = cur_node.next
