class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = Node()

    # Adds a node (data) to the linked list
    def append(self, data):
        new_node = Node(data)
        cur_node = self.head
        while(cur_node.next != None):
            cur_node = cur_node.next
        cur_node.next = new_node

    # Prints all data in linked list
    def display(self):
        elements = []
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
            elements.append(cur_node.data)
        print(elements)

    # Returns length of linked list
    def length(self):
        total = 0
        cur_node = self.head
        while cur_node.next != None:
            total += 1
            cur_node = cur_node.next
        return total

    # Pull out data point from a certain index
    def get(self, index):
        if index >= self.length():
            print("Error: Get index out of range")
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
            print("Error: Erase index out of range")
            return
        cur_index = 0
        cur_node = self.head
        while True:l
            last_node = cur_node
            cur_node = cur_node.next
            if cur_index == index:
                last_node.next = cur_node.next
                return
            cur_index += 1

my_list = LinkedList()
print(my_list.length())
my_list.display()
my_list.append(0)
my_list.append(1)
my_list.append(2)
my_list.append(3)
my_list.display()
my_list.erase(1)
my_list.display()
print(my_list.length())
print(my_list.get(0))
