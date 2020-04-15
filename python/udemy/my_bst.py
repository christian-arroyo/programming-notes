class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Assuming no duplicate values are inserted
class Bst:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root == None:
            self.root = new_node
        else:
            cur_node = self.root
            while True:
                # traversing left
                if value < cur_node.value:
                    if not cur_node.left:
                        cur_node.left = new_node
                        return self
                    else:
                        cur_node = cur_node.left
                # traversing right
                elif value > cur_node.value:
                    if not cur_node.right:
                        cur_node.right = new_node
                        return self
                    else:
                        cur_node = cur_node.right

    # return True if element exists, false otherwise
    def lookup(self, value):
        cur_node = self.root
        while True:
            if cur_node == None:
                return False
            if cur_node.value == value:
                return True
            elif value < cur_node.value:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right

    def print_tree(self):
        self.printt(self.root)

    def printt(self, cur_node):
        if cur_node != None:
            self.printt(cur_node.left)
            print(str(cur_node.value))
            self.printt(cur_node.right)

    # Will give you output of numbers in BFS order
    def breadth_first_search(self):
        cur_node = self.root
        answer = []
        level_queue = []
        level_queue.append(cur_node)

        while len(level_queue) > 0:
            cur_node = level_queue[0]
            print(cur_node.value)
            del level_queue[0]
            answer.append(cur_node)
            if cur_node.left:
                level_queue.append(cur_node.left)
            if cur_node.right:
                level_queue.append(cur_node.right)

    # def breadth_first_search_recursive(self, queue, list):



bst = Bst()
bst.insert(10)
bst.insert(5)
bst.insert(6)
bst.insert(12)
bst.insert(8)
print(bst.lookup(6))
print(bst.lookup(12))
print(bst.lookup(7))
# bst.print_tree()
bst.breadth_first_search()
