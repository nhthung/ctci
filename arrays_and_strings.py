from collections import Counter
from pprint import pprint

'''
Is Unique:
Implement an algorithm to determine if a string has all unique characters.
What if you cannot use additional data structures?
'''
def is_unique(s):
    '''
    Assuming checking string of ASCII characters
    '''
    cc = []

    # 128 ASCII characters
    charset_size = 128

    # If string length exceeds 256, then there's a duplicate
    if len(s) > charset_size:
        return False

    for c in s:
        if c in cc:
            return False
        else:
            cc.append(c)
    
    return True

def is_unique_2(s):
    '''
    Reduce space usage by using bitwise operators
    Assuming string of lowercase letters a-z
    '''
    checker = 0
    
    for c in s:
        val = ord(c) - ord('a')

        if checker & (1 << val) > 0:
            return False    
        checker |= 1 << val
    
    return True


'''
Check Permutation:
Given two strings, write a method to decide if one is a permutation of the
other.
'''
def is_permutation(s1, s2):
    count = {}

    # If strings have different lengths,
    # they aren't permuations of one another
    if len(s1) != len(s2):
        return False

    for c in s1:
        if c in count:
            count[c] += 1
        else:
            count[c] = 1

    for c in s2:
        if c in count:
            count[c] -= 1
            if count[c] < 0:
                return False
        else:
            return False
    
    return True

assert is_permutation('HELLO', 'ELLHO') == True
assert is_permutation('HELLOH', 'ELLHO') == False
assert is_permutation('HELLOH', 'ELLHOL') == False

'''
URLify:
Write a method to replace all spaces in a string with '%20'. You may assume that the string
has sufficient space at the end to hold the additional characters, and that you are given the "true"
length of the string.
'''
def urlify(s):
    return s.strip().replace(' ', '%20')

assert urlify('Mr  Anderson  ') == 'Mr%20%20Anderson'


'''
Palindrome Permutation:
Given a string, write a function to check if it is a permutation of a palin­
drome. A palindrome is a word or phrase that is the same forwards and backwards. A permutation
is a rearrangement of letters. The palindrome does not need to be limited to just dictionary words.
'''
def is_palindrome_permutation(s):
    count = {}
    num_odds = 0

    s = s.replace(' ', '')

    for c in s:
        if c in count:
            count[c] += 1
        else:
            count[c] = 1
    
    for c in count:
        if count[c] % 2 == 1:
            num_odds += 1
        
        if num_odds > 1:
            return False
    
    return True

assert is_palindrome_permutation('taco cat') == True
assert is_palindrome_permutation('taco catt') == False

def is_palindrome_permutation_2(s):
    '''
    Instead of checking the number of odd counts at the end, we can check as we go along. Then, as soon as
    we get to the end, we have our answer.
    '''
    count = {}
    num_odds = 0

    s = s.replace(' ', '')

    for c in s:
        if c in count:
            count[c] += 1
        else:
            count[c] = 1
        
        if count[c] % 2 == 1:
            num_odds += 1
        else:
            num_odds -= 1
    
    return num_odds <= 1

assert is_palindrome_permutation_2('taco cat') == True
assert is_palindrome_permutation_2('taco catt') == False

def is_palindrome_permutation_3(s):
    '''
    Using bitwise operators
    To check that no bits in the integer are 1: just compare the integer to 0.
    To check that an integer has exactly one bit set to 1:
        subtract 1 from the number
        then AND it with the new number, we should get 0.

        00010000 - 1 = 00001111
        00010000 & 00001111 = 0
    
    Assume ASCII letters from a-z
    '''
    bit_vector = 0

    def toggle_bit(bit_vector, c):
        mask = 1 << (ord(c) - ord('a'))
        
        if bit_vector & mask == 0:
            bit_vector |= mask
        else:
            bit_vector &= ~mask
        
        return bit_vector

    def has_exactly_one_bit_set(bit_vector):
        return bit_vector & (bit_vector - 1) == 0

    s = s.replace(' ', '')

    for c in s:
        bit_vector = toggle_bit(bit_vector, c)
    
    return bit_vector == 0 or has_exactly_one_bit_set(bit_vector)

assert is_palindrome_permutation_3('taco cat') == True
assert is_palindrome_permutation_3('taco catt') == False


'''
One Away:
There are three types of edits that can be performed on strings: insert a character,
remove a character, or replace a character. Given two strings, write a function to check if they are
one edit (or zero edits) away.
'''
def is_one_away(s1, s2):
    if s1 == s2:
        return True
    
    if abs(len(s1) - len(s2)) > 1:
        return False
    
    def is_one_replace(s1, s2):
        '''
        One replacement away means same length and at most one difference
        '''
        found_diff = False
        for c1, c2 in zip(s1, s2):
            if c1 != c2:
                if found_diff:
                    return False
                found_diff = True
        
        return True

    def is_one_insert(s1, s2):
        '''
        One replacement/deletion means length diff of 1
        '''
        idx1, idx2 = 0, 0
        while idx1 < len(s1) and idx2 < len(s2):
            if s1[idx1] != s2[idx2]:
                if idx1 != idx2:
                    return False
                idx2 += 1
            else:
                idx1 += 1
                idx2 += 1
        
        return True

    if len(s1) == len(s2):
        return is_one_replace(s1, s2)
    else:
        shorter_str, longer_str = (s1, s2) if len(s1) < len(s2) else (s2, s1)
        return is_one_insert(shorter_str, longer_str)

assert is_one_away('abc', 'abcd') == True
assert is_one_away('bcd', 'abcd') == True
assert is_one_away('abc', 'abd') == True
assert is_one_away('abc', 'abdd') == False


'''
String Compression:
Implement a method to perform basic string compression using the counts
of repeated characters. For example, the string aabcccccaaa would become a2blc5a3. If the
"compressed" string would not become smaller than the original string, your method should return
the original string. You can assume the string has only uppercase and lowercase letters (a - z).
'''
def compress_string(s):
    compressed_str = []
    count = 0
    char = ''
    for c in s:
        if c != char:
            if count > 0:
                compressed_str.append(str(count))
                count = 0

            compressed_str.append(c)
            char = c
        count += 1
    
    compressed_str.append(str(count))
    compressed_str = ''.join(compressed_str)
    
    return compressed_str if len(compressed_str) <= len(s) else s


'''
Rotate Matrix:
Given an image represented by an NxN matrix, where each pixel in the image is 4
bytes, write a method to rotate the image by 90 degrees. Can you do this in place?
'''
def rotate_mat(mat):
    '''
    TODO
    '''
    if len(mat) == 0 or len(mat) != len(mat[0]):
        raise ValueError

    n = len(mat)
    for layer in range(n/2):
        first = layer
        last = n - 1 - layer

        pass


'''
Zero Matrix:
Write an algorithm such that if an element in an MxN matrix is 0, its entire row and
column are set to 0.
'''
def zero_mat(mat):
    '''
    TODO
    '''
    pass