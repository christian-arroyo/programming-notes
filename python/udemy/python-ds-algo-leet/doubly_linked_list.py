from typing import Optional

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self, value) -> None:
        new_node =  Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1
    
    def print_list(self) -> None:
        temp = self.head
        while temp is not None:
            print(temp.value, end='->')
            temp = temp.next
        print("")

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.tail = self.head = new_node
        else:       
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1
        return True

    def pop(self) -> Node:
        if self.length == 0:
            return None
        temp = self.tail
        if self.length == 1:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            temp.prev = None
        self.length -= 1
        return temp
    
    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1
        return True
    
    def pop_first(self):
        if self.length == 0:
            return None
        temp = self.head
        if self.length == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
            temp.next = None
        self.length -= 1
        return temp
    
    def get(self, index) -> Optional[int]:
        if index < 0 or index >= self.length:
            return None
        cur = self.head
        if index < self.length/2:
            for _ in range(index):
                cur =  cur.next
        else:
            cur = self.tail
            for _ in range(self.length - index - 1):
                cur = cur.prev    
        return cur
    
    def set_value(self, index, value) -> bool:
        cur = self.get(index)
        if cur:
            cur.value = value
            return True
        return False


my_doubly_linked_list = DoublyLinkedList(0)
my_doubly_linked_list.append(1)
my_doubly_linked_list.append(2)
my_doubly_linked_list.append(3)
my_doubly_linked_list.append(4)
my_doubly_linked_list.print_list()
my_doubly_linked_list.pop()
my_doubly_linked_list.print_list()
my_doubly_linked_list.pop_first()
my_doubly_linked_list.print_list()
print(my_doubly_linked_list.get(1).value)

