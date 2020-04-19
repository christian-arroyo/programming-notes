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

    # Will give you output of numbers in BFS order, recursively
    def breadth_first_search_recursive(self, queue, list):
        if len(queue) == 0:
            return list
        cur_node = queue[0]
        print(cur_node.value)
        del queue[0]
        list.append(cur_node)
        if cur_node.left:
            queue.append(cur_node.left)
        if cur_node.right:
            queue.append(cur_node.right)
        return self.breadth_first_search_recursive(queue, list)

    def dfs_in_order(self):
        return self.traverse_in_order(self.root, [])

    def traverse_in_order(self, node, answers):
        if node.left:
            self.traverse_in_order(node.left, answers)
        answers.append(node.value)
        if node.right:
            self.traverse_in_order(node.right,answers)
        return answers

    def dfs_pre_order(self):
        return self.traverse_pre_order(self.root, [])

    def traverse_pre_order(self, node, answers):
        answers.append(node.value)
        if node.left:
            self.traverse_pre_order(node.left, answers)
        if node.right:
            self.traverse_pre_order(node.right, answers)
        return answers

    def dfs_post_order(self):
        return self.traverse_post_order(self.root, [])

    def traverse_post_order(self, node, answers):
        if node.left:
            self.traverse_post_order(node.left, answers)
        if node.right:
            self.traverse_post_order(node.right, answers)
        answers.append(node.value)
        return answers



#     9
#   4    20
# 1  6 15  170
# inorder - [1,4 6,9,15,20,170]
# preorder - [9,4,1,6,20,15,170]
# postorder - [1,6,4,15,170,20,9]

tree = Bst()
tree.insert(9)
tree.insert(4)
tree.insert(6)
tree.insert(20)
tree.insert(170)
tree.insert(15)
tree.insert(1)

# print(tree.lookup(12))
# print(tree.lookup(7))
# tree.print_tree()
# tree.breadth_first_search()
# tree.breadth_first_search_recursive([tree.root], [])
print(tree.dfs_in_order())
print(tree.dfs_pre_order())
print(tree.dfs_post_order())
