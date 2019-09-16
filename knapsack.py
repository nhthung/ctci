from pprint import pprint

def knapsack(weights, values, max_weight):
    '''
    Duplicates allowed variant
    O(n_items * max_weight) time
    '''
    n = len(weights)

    # K stores max value at each subweight from 0 to max_weight
    K = [0] * (max_weight + 1)

    for weight_limit in range(1, max_weight + 1):
        for weight, value in zip(weights, values):
            if weight <= weight_limit:
                cur_value = K[weight_limit - weight] + value
                
                if cur_value > K[weight_limit]:
                    K[weight_limit] = cur_value
    return K

'''
| Item | Weight | Value |
|------|--------|-------|
| 1    | 2      | 1     |
| 2    | 10     | 20    |
| 3    | 3      | 3     |
| 4    | 6      | 14    |
| 5    | 18     | 100   |

'''
max_weight = 15
weights = [2, 10, 3, 6, 18]
values = [1, 20, 3, 14, 100]

K = knapsack(weights, values, max_weight)
assert K == [0, 0, 1, 3, 3, 4, 14, 14, 15, 17, 20, 20, 28, 28, 29, 31]

def knapsack_2(weights, values, max_weight):
    '''
    No dupicates allowed variant
    O(n_items * max_weight) time
    '''
    # Prepend item with 0 weight and value
    weights = [0] + weights
    values = [0] + values

    n = len(weights)
    K = [[0 for _ in range(max_weight + 1)] for _ in range(n)]

    # for i, (weight, value) in enumerate(zip(weights, values)):
    for i in range(1, n):
        weight = weights[i]
        value = values[i]

        for weight_limit in range(1, max_weight + 1):
            if weight <= weight_limit:
                K[i][weight_limit] = max(K[i - 1][weight_limit - weight] + value,
                                        K[i - 1][weight_limit])
            else:
                K[i][weight_limit] = K[i - 1][weight_limit]
    return K

def traceback(K, weights):
    '''
    Return items that were added in knapsack

    Travel table from bot to top row, right to left column
    Cell value didn't come from cell directly above => item was added
        => Move left from cur column w to column w - wi (wi weight of added item)
    Go up by 1 row, repeat
    '''
    n = len(K) - 1
    W = len(K[0]) - 1

    weights = [0] + weights

    items = []
    w = W
    for i in range(n, 0, -1):
        if K[i][w] != K[i - 1][w]:
            items.append(i)
            w -= weights[i]
    
    return items

K = knapsack_2(weights, values, max_weight)
assert K[-1][-1] == 24