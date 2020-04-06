class Stack:
    def __init__(self):
        self.array = []

    def push(self, value):
        self.array.append(value)

    def peek(self):
        return self.array[-1]

    def pop(self):
        self.array.pop()

    def print_stack(self):
        for e in self.array:
            print(e, end='->')


s = Stack()
s.push("google")
s.push("youtube")
s.push("udemy")
print(s.peek())
s.print_stack()
