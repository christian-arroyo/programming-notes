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
        if self.root = None:
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
        if self.root == None:
            return False
        cur_node = self.root
        while cur_node:
            if cur_node.value < value:
                cur_node = cur_node.left
            elif cur_node.value > value:
                cur_node = cur_node.right
            elif cur_node.value == value:
                return True
        return False

    # Was not able to finish it
    
    # def remove(self, value):
    #     if self.root == None:
    #         return False
    #     cur_node = self.root
    #     while cur_node:
    #         if cur_node.value < value:
    #             parent_node = cur_node
    #             cur_node.left = cur_node
    #         elif cur_node.value > value:
    #             parent_node = cur_node
    #             cur_node.right = cur_node
    #         # Found node in the list
    #         elif cur_node.value == value:
    #             # Option 1: No right child
    #             if cur_node.right == None:
    #                 if parent_node
    #             # Option 2: Right child which doesn't have a left child
    #             # Option 3: Right child that has a left child

        print("Error - remove - value does not exist in tree")
        return False
