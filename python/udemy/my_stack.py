class Node:
    def __init__(self, value):
        self.next = None
        self.value = value

class Stack:
    def __init__(self):
        self.bottom = None
        self.top = None
        self.length = 0

    def peek(self):
        return self.top

    def push(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.bottom = new_node
            self.top = new_node
        elif self.length > 0:
            cur_node = self.top
            cur_node.next = new_node
            self.top = new_node
        self.length += 1
        return self

    def print_stack(self):
        cur_node = self.bottom
        if self.length == 0:
            return None
        while(cur_node):
            print(cur_node.value, end=' -> ')
            cur_node = cur_node.next

    def pop(self):
        if self.top == None:
            return None
        value = self.top.value
        self.top = None
        self.length -= 1
        return value


s = Stack()
s.push("google")
s.push("udemy")
s.push("youtube")
s.print_stack()
