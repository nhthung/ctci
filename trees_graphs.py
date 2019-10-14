import math
from stacks_queues import QueueFromStacks
from utils.trees import BSTNode, print_bst

def in_order(node):
    pass

def bfs(node):
    pass

def bidirectional(node):
    pass


'''
Route Between Nodes:
Given a directed graph, design an algorithm to find out whether there is a
route between two nodes.
'''
def has_path(graph, start, end):
    if start == end:
        return True

    for node in graph.nodes:
        node.state = State.unvisited

    queue = QueueFromStacks()
    start.state = State.visiting
    queue.enqueue(start)
    
    while not queue.is_empty():
        visiting = queue.dequeue()
        if visiting:
            for node in visiting.adjacent:
                if node.state == State.unvisited:
                    if node == end:
                        return True
                    else:
                        node.state = State.visiting
                        queue.enqueue(node)
            visiting.state = State.visited
    return False

class State:
    unvisited = 'Unvisited'
    visited = 'Visited'
    visiting = 'Visiting'


'''
Minimal Tree:
Given a sorted (increasing order) array with unique integer elements, write an
algorithm to create a binary search tree with minimal height
'''
def arr_to_bst(arr):
    n = len(arr)

    if n == 0:
        return None

    root_idx = math.floor(n / 2)
    root = BSTNode(data=arr[root_idx])

    if n == 2:
        root.left = BSTNode(data=arr[0])
    
    elif n > 2:
        root.left = arr_to_bst(arr[:root_idx])
        root.right = arr_to_bst(arr[root_idx + 1:])

    return root


if __name__ == '__main__':
    arr = [-100,2,3,4,5,6,100]
    root = arr_to_bst(arr)
    print_bst(root)