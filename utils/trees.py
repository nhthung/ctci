from linked_lists import LinkedList, print_ll

class Node:
    def __init__(self, data):
        self.data = data

class BSTNode(Node):
    '''
    BST node
    '''
    def __init__(self, data, left=None, right=None):
        super().__init__(data)
        self.left = left
        self.right = right


def print_bst(root):
    '''
    Print complete BST by level
    '''
    if not root:
        return

    queue = LinkedList()
    print(root.data)
    queue.add(root)

    while not queue.is_empty():
        # Dequeue
        visiting = queue.pop(idx=0).data

        if visiting.left:
            print(visiting.left.data, end=', ')
            queue.add(visiting.left)
            
        if visiting.right:
            print(visiting.right.data, end=', ')
            queue.add(visiting.right)
            
            if visiting.right.data > queue.peek(idx=0).data.data:
                print()
    print()