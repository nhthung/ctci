def binary_search(vals, val):
    if len(vals) == 1:
        return vals[0] if vals[0] == val else 'Value not found'
    
    mid = len(vals) // 2
    if val >= vals[mid]:
        return binary_search(vals[mid:], val)
    else:
        return binary_search(vals[:mid], val)

def mergesort():
    pass

def quicksort():
    pass