class Node:
    def __init__(self, d):
        self.data = d
        self.next = None

class Queue:
    def __init__(self):
        self.first = None
        self.last = None
        self.length = 0

    def dequeue(self):
        if self.is_empty():
            return None
        elif self.first == self.last:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
            self.length -= 1

    def enqueue(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.first = new_node
            self.last = new_node
        else:
            former_last = self.last
            former_last.next = new_node
            self.last = new_node
        self.length += 1

    def is_empty(self):
        return False if self.length else True

    def peek(self):
        return self.first.data

    def print_queue(self):
        cur_node = self.first
        while(cur_node):
            print(cur_node.data, end=' ')
            cur_node = cur_node.next


q = Queue()
print(q.length)
q.enqueue(1)
q.enqueue(2)
q.enqueue(4)
q.enqueue(9)
print(q.length)
q.print_queue()
print("")
q.dequeue()
q.print_queue()
