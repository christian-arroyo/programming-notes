class Node:
    def __init__(self, d):
        self.data = d
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.bottom = None
        self.length = 0

    def peek(self):
        return self.top.data

    def push(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.top = new_node
            self.bottom = new_node
        else:
            old_top = self.top
            self.top = new_node
            self.top.next = old_top
        self.length += 1
        return self

    def pop(self):
        if self.is_empty():
            return None
        else:
            if self.top == self.bottom:
                self.bottom = None
            old_top = self.top
            self.top = old_top.next
            self.length -= 1
            return this

    def is_empty(self):
        return False if self.length else True

    def print_stack(self)


s = Stack()
s.push('google')
s.push('udemy')
s.push('discord')
print(s.peek())
