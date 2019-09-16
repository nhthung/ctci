class LinkedList:
    '''
    Singly linked list
    '''
    def __init__(self, head=None):
        self.head = head
    
    def add(self, data):
        cur = self.head
        while cur.next:
            cur = cur.next
        
        cur.next = Node(data)

        return self
    
    def pop(self, idx=None):
        cur = self.head
        cur_idx = 0

        if idx == 0:
            popped = cur
            self.head = cur.next
            popped.next = None
        else:
            while cur.next and cur.next.next:
                if idx and idx == cur_idx + 1:
                    break

                cur = cur.next
                cur_idx += 1
            
            popped = cur.next
            cur.next = cur.next.next
            popped.next = None

        return popped
        
    def __str__(self):
        l = []
        cur = self.head

        while cur.next:
            l.append(cur.data)
            cur = cur.next
        
        l.append(cur.data)

        return str(l)


class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

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


def concat(ll1, ll2):
    cur = ll1.head
    while cur.next:
        cur = cur.next
    
    cur.next = ll2.head
    ll = ll1
    return ll


def make_ll(list):
    ll = LinkedList(head=Node(list[0]))

    if len(list) > 1:
        for el in list[1:]:
            ll.add(el)
    
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

def make_list(ll):
    l = []
    cur = ll.head

    while cur:
        l.append(cur.data)
        cur = cur.next
    
    return l

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
def k_to_last(ll):
    pass