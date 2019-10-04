from utils.linked_lists import *


def weave(ll1, ll2):
    '''
    Apply 'Runner Technique':
        one pointer p1 (the fast pointer) move every two elements for every one move that p2
        makes. When p1 hits the end of the linked list, p2 will be at the midpoint. Then, move pl back to the front
        and begin "weaving" the elements. On each iteration, p2 selects an element and inserts it after p1.
    '''
    # Concatenate two linked lists
    ll = concat(ll1, ll2)

    p1, p2 = ll.head, ll.head
    while p1.next.next:
        p2 = p2.next
        p1 = p1.next.next

    p1 = ll.head

    while p1 != p2:
        t1 = p1.next
        t2 = p2.next

        p1.next = t2
        p2.next = t2.next
        t2.next = t1
        
        p1 = t1
    
    return ll


l1 = [1, 2, 3, 4, 5, 6]
l2 = ['a', 'b', 'c', 'd', 'e', 'f']

ll1 = make_ll(l1)
ll2 = make_ll(l2)

assert str(weave(ll1, ll2)) == "[1, 'a', 2, 'b', 3, 'c', 4, 'd', 5, 'e', 6, 'f']"


'''
Remove Dups:
Write code to remove duplicates from an unsorted linked list.
FOLLOW UP
How would you solve this problem if a temporary buffer is not allowed?
'''
def remove_dups(ll):
    '''
    Iterate once, use extra space
    O(1) time, O(n) space
    '''
    cur = ll.head
    found = []
    prev = None
    removed = None

    while cur:
        if cur.data in found:
            prev.next = cur.next
            removed = cur
        else:
            found.append(cur.data)
            prev = cur

        cur = cur.next
        
        if removed:
            removed.next = None
        else:
            removed = None
    
    return ll

ll = make_ll([1,1,2,3,3,4])
assert make_list(remove_dups(ll)) == [1,2,3,4]

def remove_dups_2(ll):
    '''
    No extra space.
    O(n^2) time, O(1) space
    '''
    cur = ll.head

    while cur:
        runner = cur
        while runner.next:
            if runner.next.data == cur.data:
                runner.next = runner.next.next
            else:
                runner = runner.next
        cur = cur.next
    
    return ll

assert make_list(remove_dups_2(ll)) == [1,2,3,4]


'''
Return Kth to Last:
Implement an algorithm to find the kth to last element of a singly linked list.
'''
def k_to_last(ll, k):
    length = 0
    cur = ll.head

    while cur:
        cur = cur.next
        length += 1
    
    if k > length:
        raise ValueError('k exceeds length of list')

    cur = ll.head
    for i in range(length - k):
        cur = cur.next
    
    return cur.data

ll = make_ll([1,1,2,3,3,4])
assert k_to_last(ll, k=4) == 2


'''
Delete Middle Node:
Implement an algorithm to delete a node in the middle (i.e., any node but
the first and last node, not necessarily the exact middle) of a
singly linked list, given only access to that node.
'''
def del_middle(node):
    pass

ll = make_ll([1,1,2,3,3,4])

# Want to delete 3rd node


'''
Partition:
Write code to partition a linked list around a value x, such that all nodes less than x come
before all nodes greater than or equal to x. If x is contained within the list, the values of x only need
to be after the elements less than x (see below). The partition element x can appear anywhere in the
"right partition"; it does not need to appear between the left and right partitions.
'''
def partition(ll, x):
    head = ll.head
    tail = ll.head

    cur = ll.head
    while cur:
        nxt = cur.next
        if cur.data < x:
            cur.next = head
            head = cur
            ll.head = head
        else:
            tail.next = cur
            tail = cur
        cur = nxt
    tail.next = None

    return ll

ll = make_ll([3,5,8,5,10,2,1])
assert make_list(partition(ll, x=8)) == [1, 2, 5, 5, 3, 8, 10]


def add_ll(l1_node, l2_node, carry=0):
    if l1_node == l2_node == None and carry == 0:
        return
    
    value = carry

    if l1_node:
        value += l1_node.data
    if l2_node:
        value += l2_node.data
    
    result = Node(value % 10)

    if l1_node or l1_node:
        result.next = add_ll(
            l1_node.next if l1_node else None,
            l2_node.next if l2_node else None,
            1 if value >= 10 else 0
        )
    
    return result

l1 = make_ll([7,1,6])
l2 = make_ll([5,9,2])
assert make_list(LinkedList(add_ll(l1.head, l2.head))) == [2, 1, 9]