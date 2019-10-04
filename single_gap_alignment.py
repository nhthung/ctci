import math
from utils.single_gap_alignment import *


def main():
    match_score = 1
    mismatch_score = -1
    b = -1
    filenames = (
        'alignment/hw1_short.fa',
        'alignment/hw1_medium.fa',
        # 'alignment/hw1_long.fa',
    )
    for filname in filenames:
        multi_gap_free(filname, match_score, mismatch_score, b)


def multi_gap_free(filename, match_score, mismatch_score, b):
    # Substitution cost matrix
    s = lambda Sj, Ti : match_score if Sj == Ti else mismatch_score
    seqs = load_fa(filename)
    S, T = seqs['S']['seq'], seqs['T']['seq']

    M, S_gap, T_gap, back_ptrs = _multi_gap_free(S, T, s, b)
    alignments = traceback(M, S_gap, T_gap, back_ptrs, S, T)
    score = score_alignment(M, S_gap, T_gap)

    S_name = seqs['S']['name']
    T_name = seqs['T']['name']

    idx_to_name = {
        0: S_name,
        1: T_name 
    }
    print(f'{filename}:')
    print(f'Score: {score}\n')
    print_alignments(alignments, idx_to_name)
    print('-' * 20)


def _multi_gap_free(S, T, s, b):
    '''
    :param S: Sequence spanning columns (top)
    :param T: Sequence spanning rows (left)
    :param s: Substitution cost matrix
    :param b: Gap penalty cost
    '''
    m, n = len(S), len(T)

    if not n >= m >= math.ceil(n/2):
        err_msg = 'Lengths m, n of S, T need to fulfill n >= m >= ceil(n/2)'
        raise ValueError(err_msg)
    
    M = init_M(m, n)
    S_gap = init_S_gap(m, n, b)
    T_gap = init_T_gap(m, n, b)
    back_ptrs = init_back_ptrs(m, n)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            Ti = T[i-1]
            Sj = S[j-1]

            fill_M(M, S_gap, T_gap, back_ptrs, Ti, Sj, i, j, s)
            fill_S_gap(M, S_gap, T_gap, back_ptrs, i, j, b)
            fill_T_gap(M, S_gap, T_gap, back_ptrs, i, j, b)
    
    return M, S_gap, T_gap, back_ptrs


def traceback(M, S_gap, T_gap, back_ptrs, S, T):
    alignments = []

    idx_to_table = {
        0: 'M',
        1: 'S_gap',
        2: 'T_gap'
    }
    tables = (M, S_gap, T_gap)
    i, j = len(T), len(S)

    max_score = score_alignment(M, S_gap, T_gap)

    start_tables = [
        idx_to_table[idx]
        for idx, table in enumerate(tables)
        if table[i][j] == max_score
    ]
    
    for start_table in start_tables:
        if start_table == 'M':
            alignment = [S[-1], T[-1]]
            _S = S[:-1]
            _T = T[:-1]

        elif start_table == 'S_gap':
            alignment = ['-', T[-1]]
            _S = S
            _T = T[:-1]
            
        elif start_table == 'T_gap':
            alignment = [S[-1], '-']
            _S = S[:-1]
            _T = T

        _traceback(back_ptrs, start_table, i, j, _S, _T, alignment, alignments)

    return alignments


def _traceback(back_ptrs, ptrs_table, i, j, S, T, alignment, alignments):
    ptrs = back_ptrs[ptrs_table][i][j]

    back_ij = {
        'M'    : (i-1, j-1),
        'S_gap': (i-1, j),
        'T_gap': (i, j-1),
    }
    back_i, back_j = back_ij[ptrs_table]

    if i == 0 or j == 0:
        alignments.append(alignment)
    else:
        try:
            if 'M' in ptrs:
                _traceback(
                    back_ptrs, 'M',
                    back_i, back_j,
                    S[:-1], T[:-1],
                    [S[-1] + alignment[0], T[-1] + alignment[1]],
                    alignments
                )
            if 'S_gap' in ptrs:
                _traceback(
                    back_ptrs, 'S_gap',
                    back_i, back_j,
                    S, T[:-1],
                    ['-' + alignment[0], T[-1] + alignment[1]],
                    alignments
                )
            if 'T_gap' in ptrs:
                _traceback(
                    back_ptrs, 'T_gap',
                    back_i, back_j,
                    S[:-1], T,
                    [S[-1] + alignment[0], '-' + alignment[1]],
                    alignments
                )    
        except:
            alignments.append(alignment)
    

if __name__ == '__main__':
    main()