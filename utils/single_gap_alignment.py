# Author: Le Nhat Hung
# ID    : 260793376

from Bio import SeqIO


def load_fa(filename):
    '''
    Return dict of keys 'S' and 'T',
    values {'name': ..., 'seq': ...},
    with S containing the shorter sequence
    '''
    fasta_seqs = SeqIO.parse(open(filename), 'fasta')
    name_seqs = [(fasta.id, str(fasta.seq)) for fasta in fasta_seqs]
    S = 0 if len(name_seqs[0][1]) <= len(name_seqs[1][1]) else 1
    T = 0 if S == 1 else 1

    seqs = {
        'S': {'name': name_seqs[S][0], 'seq': name_seqs[S][1]},
        'T': {'name': name_seqs[T][0], 'seq': name_seqs[T][1]}
    }
    return seqs


def score_alignment(M, S_gap, T_gap):
    return max(table[-1][-1] for table in (M, S_gap, T_gap))


def print_alignments(alignments, idx_to_names):
    num_alns = len(alignments)
    if num_alns > 1:
        print(f'{num_alns} alignments found:\n')

    for i, (S_aligned, T_aligned) in enumerate(alignments):
        if num_alns > 1:
            print(f'Alignment {i+1}:')

        print(f'{idx_to_names[0]}: {S_aligned}')
        print(f'{idx_to_names[1]}: {T_aligned}\n')


def fill_M(M, S_gap, T_gap, back_ptrs, Ti, Sj, i, j, s):
    vals = (
        M[i-1][j-1],
        S_gap[i-1][j-1],
        T_gap[i-1][j-1],
    )
    M[i][j] = s(Ti, Sj) + max(vals)
    
    # fill_back_ptrs(back_ptrs, 'M', vals, i, j)

    return M


def fill_S_gap(M, S_gap, T_gap, back_ptrs, i, j, b):
    vals = (M[i-1][j], T_gap[i-1][j])
    S_gap[i][j] = max(vals) + b

    # fill_back_ptrs(back_ptrs, 'S_gap', vals, i, j)
    
    return S_gap


def fill_T_gap(M, S_gap, T_gap, back_ptrs, i, j, b):
    vals = (M[i][j-1], S_gap[i][j-1])
    T_gap[i][j] = max(vals) + b
    
    # fill_back_ptrs(back_ptrs, 'T_gap', vals, i, j)

    return T_gap


def fill_back_ptrs(back_ptrs, table, vals, i, j):
    ptrs = []
    idx_to_table = None
    max_val = max(vals)

    if table == 'M':
        idx_to_table = {
            0: 'M',
            1: 'S_gap',
            2: 'T_gap',
        }
    elif table == 'S_gap':
        idx_to_table = {
            0: 'M',
            1: 'T_gap'
        }
    elif table == 'T_gap':
        idx_to_table = {
            0: 'M',
            1: 'S_gap'
        }

    if idx_to_table:
        ptrs = [
            idx_to_table[idx]
            for idx, val in enumerate(vals)
            if val == max_val
        ]
    
    back_ptrs[table][i][j] = ptrs
    return back_ptrs


def init_M(m, n):
    '''
    M[0,j] = "score of best alignment between
              0 chars of T and j chars of S
              that ends in a match"
           = -infinity
             because there can't be a match with 0 chars of T,
             therefore such alignments don't exist
		          
    Same reasoning with M[i,0]
    '''
    M = init_table(m, n)
    M[0][0] = 0
    
    return M


def init_S_gap(m, n, b):
    '''
    S_gap[0,j] has the same reasoning as T_gap[i,0]
    S_gap[i,0] has the same reasoning as T_gap[0,j]
    '''
    S_gap = init_table(m, n)
    S_gap[1][0] = b
    
    return S_gap
    

def init_T_gap(m, n, b):
    '''
    :param b: Gap penalty cost

    T_gap[0,j] = "score of best alignment between
                  0 chars of T and j chars of S
                  that ends in a gap in T"
               = b if j == 1 else -infinity
    
    When j == 1, the alignment looks like:
        s
        -
        which is allowed
    
    When j != 1:
        ssss
        ----
        which isn't allowed
    
    T_gap[i, 0] = "score of best alignment between
                   i chars of T and 0 chars of S
                   that ends in a gap in T"
                = -infinity
                   because with 0 chars of S, the gap in T
                   will align with another gap in S, which isn't allowed
    
    This alignment looks like:
        ----
        ttt-
    '''
    T_gap = init_table(m, n)
    T_gap[0][1] = b

    return T_gap


def init_back_ptrs(m, n):
    tables = ('M', 'S_gap', 'T_gap')
    back_ptrs = {table: init_table(m, n) for table in tables}
    return back_ptrs


def init_table(m, n):
    '''
    Initialize table with width m+1 and height n+1
    '''
    return [[float('-inf') for j in range(m+1)] for i in range(n+1)]


def print_table(table):
    for row in table:
        print(row)