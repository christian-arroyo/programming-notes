class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.back = None
        self.front = None
        self.length = 0

    def peek(self):
        return self.front.value

    # Add to back of linkedlist
    def enqueue(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.front = new_node
            self.back = new_node
            self.length = 1
        else:
            self.back.next = new_node
            self.back = new_node
            self.length += 1

    def dequeue(self):
        if self.length == 0:
            return None
        else:
            first_node = self.front
            self.front = self.front.next
            return first_node

    def print_queue(self):
        cur_node = self.front
        while cur_node:
            print(cur_node.value, end="->")
            cur_node = cur_node.next

q = Queue()
q.enqueue("David")
q.enqueue("Christian")
q.enqueue("Jessica")
q.enqueue("Chuy")
# q.print_queue()
q.dequeue()
q.print_queue()
