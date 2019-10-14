class LinkedList:
    '''
    Singly linked list
    '''
    def __init__(self, head=None):
        self.head = head
    
    def add(self, data):
        cur = self.head

        if not cur:
            self.head = Node(data)
            return self

        while cur.next:
            cur = cur.next
        
        cur.next = Node(data)

        return self
    
    def pop(self, idx=None):
        '''
        By default pop most recently added element.
        '''
        cur = self.head
        cur_idx = 0

        if idx == 0 or self.head.next is None:
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

    def peek(self, idx=None):
        cur = self.head
        cur_idx = 0

        if idx == 0 or self.head.next is None:
            peeked = cur
        else:
            while cur.next and cur.next.next:
                if idx and idx == cur_idx + 1:
                    break

                cur = cur.next
                cur_idx += 1
            
            peeked = cur.next

        return peeked

    def is_empty(self):
        return not self.head
        
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


def make_ll(list):
    ll = LinkedList(head=Node(list[0]))

    if len(list) > 1:
        for el in list[1:]:
            ll.add(el)
    
    return ll


def concat(ll1, ll2):
    cur = ll1.head
    while cur.next:
        cur = cur.next
    
    cur.next = ll2.head
    ll = ll1
    return ll


def make_list(ll):
    l = []
    cur = ll.head

    while cur:
        l.append(cur.data)
        cur = cur.next
    
    return l

def print_ll(ll):
    print(make_list(ll))


if __name__ == '__main__':
    ll = make_ll([1,2])
    print(ll.pop(0).data)
    print(ll.head.data)