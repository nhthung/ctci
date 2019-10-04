class Stack:
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(StackNode(data))
        return self.stack

    def pop(self):
        return self.stack.pop().data

    def peek(self):
        return self.stack[-1].data
    
    def is_empty(self):
        return self.size == 0
    
    @property
    def size(self):
        return len(self.stack)


class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class QueueFromStacks:
    '''
    Queue implemented from 2 stacks
    '''
    def __init__(self):
        self.newest_top = Stack()
        self.oldest_top = Stack()

    def enqueue(self, data):
        if self.newest_top.is_empty():
            self.move_all(self.oldest_top, self.newest_top)
        
        self.newest_top.push(data)

    def dequeue(self):
        if self.oldest_top.is_empty():
            self.move_all(self.newest_top, self.oldest_top)
        
        return self.oldest_top.pop()
    
    def peek(self):
        if self.oldest_top.is_empty():
            self.move_all(self.newest_top, self.oldest_top)
        
        return self.oldest_top.peek()

    def move_all(self, source, sink):
        while not source.is_empty():
            sink.push(source.pop())
    
    def is_empty(self):
        return self.newest_top.is_empty() and self.oldest_top.is_empty()


def sort_stack(stack):
    '''
    Use a 2nd stack to sort elements, then pop everything back to original stack
    '''
    sorting = Stack()
    
    while not stack.is_empty():
        # Pop and hold item from original stack
        tmp = stack.pop()
        
        # If top of sorting stack larger than held item,
        # push top back to original stack, then repeat
        while (not sorting.is_empty()) and sorting.peek() > tmp:
            stack.push(sorting.pop())
        
        # Out of the while loop, the top of orting stack
        # will be <= held item.
        # Can now push held item onto sorting stack
        sorting.push(tmp)
    
    # Reverse order when done
    while not sorting.is_empty():
        stack.push(sorting.pop())
    
    return stack


class AnimalShelter:
    def __init__(self):
        self.dogs = QueueFromStacks()
        self.cats = QueueFromStacks()
        self.order = 0

    def enqueue(self, animal):
        animal.order = self.order
        self.order += 1

        if isinstance(animal, Dog):
            self.dogs.enqueue(animal)
        elif isinstance(animal, Cat):
            self.cats.enqueue(animal)

    def dequeue_any(self):
        if self.dogs.is_empty():
            return self.dequeue_cat()
        elif self.cats.is_empty():
            return self.dequeue_dog()
        
        if self.dogs.peek().is_older_than(self.cats.peek()):
            return self.dequeue_dog()
        else:
            return self.dequeue_cat()

    def dequeue_dog(self):
        return self.dogs.dequeue()

    def dequeue_cat(self):
        return self.dogs.dequeue()


class Animal:
    def __init__(self, order):
        self.order = order

    def is_older_than(self, animal):
        return self.order > animal.order

class Dog(Animal):
    def __init__(self, order):
        super().__init__(order)

class Cat(Animal):
    def __init__(self, order):
        super().__init__(order)


