class Stack:
    def __init__(self):
        self.array = []

    def push(self, data):
        self.array.append(data)

    def pop(self):
        return self.array.pop()

    def peek(self):
        return self.array[-1]
