class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = Node()

    def append(self, data):
        new_node = Node(data)
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
        cur_node.next = new_node

    def display(self):
        elements = []
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
            elements.append(cur_node.data)
        print(elements)

    def length(self):
        total = 0
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
            total += 1
        return total

    def get(self, index):
        if index >= self.length():
            print("Error - Get - Index out of bounds")
            return None
        cur_index = 0
        cur_node = self.head
        while True:
            cur_node = cur_node.next
            if cur_index == index:
                return cur_node.data
            cur_index += 1

    def erase(self, index):
        if index >= self.length():
            print("Error - Del - Index out of bounds")
            return
        cur_node = self.head
        cur_index = 0
        while True:
            last_node = cur_node
            cur_node = cur_node.next
            if cur_index == index:
                last_node.next = cur_node.next
                return
            cur_index += 1

my_list = LinkedList()
my_list.display()
my_list.append(1)
my_list.append(2)
my_list.append(3)
my_list.append(4)
my_list.display()
print(my_list.length())
print(my_list.get(2))
my_list.display()
my_list.erase(2)
my_list.display()
