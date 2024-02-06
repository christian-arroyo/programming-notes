class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def __r_insert(self, current_node, value):
        if current_node == None:
            return Node(value)
        if value < current_node.value:
            current_node.left = self.__r_insert(current_node.left, value)
        if value > current_node.value:
            current_node.right = self.__r_insert(current_node.right, value)
        # Returns just to exit from the call stack
        return current_node

    def r_insert(self, value):
        if self.root == None:
            self.root = Node(value)
        self.__r_insert(self.root, value)

    def __r_contains(self, current_node, value):
        if current_node == None:
            return False
        if value == current_node.value:
            return True
        if value < current_node.value:
            return self.__r_contains(current_node.left, value)
        if value > current_node.value:
            return self.__r_contains(current_node.right, value)


    def r_contains(self, value):
        return self.__r_contains(self.root, value)

    def minimum(self, current_node):
        while current_node.left:
            current_node = current_node.left
        return current_node.value
    



bst = BST()
bst.r_insert(2)
bst.r_insert(1)
bst.r_insert(3)
bst.r_insert(4)


print(bst.root.value)
print(bst.root.left.value)
print(bst.root.right.value)
print(bst.r_contains(0))

print(bst.minimum(bst.root))
print(bst.minimum(bst.root.right))
