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
    

    def __r_delete(self, current_node, value):
        if current_node == None:
            return None
        # Look for the node to delete, None will be assigned to left/right leaf node if value is not present
        if value < current_node.value:
            current_node.left = self.__r_delete(current_node.left, value)
        if value > current_node.value:
            current_node.right = self.__r_delete(current_node.right, value)
        # Found a match
        else:
            # Node is a leaf node
            if current_node.left == None and current_node.right == None:
                return None
            # Node to delete has left child only
            elif current_node.right == None:
                current_node = current_node.left
            # Node to delete has right child only
            elif current_node.left == None:
                current_node = current_node.right
            # Node to delete has both left and right child
            else:
                # Grab minimum value of right subtree
                sub_tree_min = self.min_value(current_node.right)
                # Assign minimum value to node to be deleted
                current_node.value = sub_tree_min
                # Delete minimum value of right subtree 
                current_node.right = self.__r_delete(current_node.right, sub_tree_min)
        return current_node


    def r_delete(self, value):
        self.__r_delete(self.root, value)

    def min_value(self, current_node):
        while current_node.left:
            current_node = current_node.left
        return current_node.value
    
    def dfs_preorder(self):
        results = []

        def traverse(current_node):
            results.append(current_node.value)
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
        traverse(self.root)
        return results

    
    def dfs_postorder(self):
        results = []

        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            if current_node.right is not None:
                traverse(current_node.right)
            results.append(current_node.value)
        
        traverse(self.root)
        return results
    
    def dfs_inorder(self):
        results = []

        def traverse(current_node):
            if current_node.left is not None:
                traverse(current_node.left)
            results.append(current_node.value)
            if current_node.right is not None:
                traverse(current_node.right)
            
        traverse(self.root)
        return results





bst = BST()
bst.r_insert(2)
bst.r_insert(1)
bst.r_insert(3)
bst.r_insert(4)



print(bst.root.value)
print(bst.root.left.value)
print(bst.root.right.value)
print(bst.r_contains(0))

print(bst.min_value(bst.root))
print(bst.min_value(bst.root.right))

bst.r_delete(55)
print("Deleting")
print(bst.root.value)
print(bst.root.left.value)
print(bst.root.right.value)
print(bst.root.right.right.value)
print(bst.dfs_preorder())
print(bst.dfs_postorder())
print(bst.dfs_inorder())
