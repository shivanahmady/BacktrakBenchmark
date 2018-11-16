import numpy as np
from datetime import datetime
import itertools
import sys

"""
n=6,  d=4: 0:00:00.004000 // answer: 4
n=7,  d=4: 0:00:00.012001 // correct answer: 8
"""

BENCHMARK = True
PIO = True
FIO = False

def det_dis(vector_1: np.array, vector_2: np.array) -> int:
    return np.count_nonzero(vector_1 != vector_2)
def genVectors(length: int, q: int=2) -> list:
    return list(map(np.array, itertools.product(list(range(q)), repeat=length)))
def gen_det_dis_T(vector_list: list, minimum_distance: int, print_result: bool=False) -> list:
    global BENCHMARK
    distance_table_timer = datetime.now()
    distance_table = []
    for needle_index, vector_needle in enumerate(vector_list):
        distance_table.append([])
        for in_stack_index, vector_in_stack in enumerate(vector_list):
            if needle_index == in_stack_index:
                is_distance = False
            elif needle_index > in_stack_index:
                is_distance = distance_table[in_stack_index][needle_index]
            else:
                is_distance = det_dis(vector_needle, vector_in_stack) >= minimum_distance
            distance_table[needle_index].append(is_distance)
    if BENCHMARK and PIO:
        print('--- distance table pre-computation time: ' + str(datetime.now() - distance_table_timer))
    if print_result:
        for row in distance_table:
            print(row)
    return distance_table
def sortingVectors(vectors_list: list) -> list:
    return sorted(vectors_list, key=np.count_nonzero)
def isWsminDOC(code: list, det_dis_list_for_word: list) -> bool:
    for codeword in reversed(code):
        if not det_dis_list_for_word[codeword]:
            return False
    return True
def backtrack(lvl: int=0) -> (int, list):
    global code, candidates, det_dis_table, promised_M, leading_bit_non_zero, q
    for lexi_index, word in enumerate(candidates[lvl]):
        det_dis_list_for_word = det_dis_table[word]
        if len(code) <= lvl:
            code.append(word)
        else:
            code[lvl] = word
        if not leading_bit_non_zero[word] and lvl >= (promised_M / q):
            return lvl, code
        if lvl + 1 >= promised_M:
            return lvl, code
        if len(candidates) <= lvl + 1:
            candidates.append([])
        else:
            candidates[lvl + 1] = []
        for candidate_for_word in candidates[lvl][lexi_index:]:
            if det_dis_list_for_word[candidate_for_word]:
                candidates[lvl + 1].append(candidate_for_word)
        if lvl + 1 + len(candidates[lvl + 1]) < promised_M:
            return lvl, code
        found_lvl, discovery = backtrack(lvl+1)
        if found_lvl + 1 >= promised_M:
            return found_lvl, discovery
    return lvl
timer = datetime.now()
q = 2
n = 7
d = 4
promised_M = 4
try:
    n = int(sys.argv[1])
except:
    pass
try:
    d = int(sys.argv[2])
except:
    pass
try:
    promised_M = int(sys.argv[3])
except:
    pass
vectors = sorted(genVectors(n, q), key=np.count_nonzero)
leading_bit_non_zero = {lexi_index: (vector[0] != 0) for lexi_index, vector in enumerate(vectors)}
# print(leading_bit_non_zero)
detailed_outputs = []
critical_outputs = []
if PIO:
    print('-----\n---\n------'+str([str(i) + ': ' + ''.join(map(str, vector)) for i, vector in enumerate(vectors)]))
det_dis_table = gen_det_dis_T(vectors, d)
init_candidates = list(range(len(vectors)))     # list of vectors indexes from 'vectors' lexi-sorted list.
code = []
candidates = [init_candidates]
max_found_M, optimalVectorIndices = backtrack()
critical_outputs.append('---\n-\n----\n === For n=' + str(n) + ' and d=' + str(d) + ' in GF(' + str(q) + '):')
detailed_outputs.append(critical_outputs[-1])
critical_outputs.append('\t\t==MAX found M is: ' + str(max_found_M + 1))
detailed_outputs.append(critical_outputs[-1])
detailed_outputs.append('==CODE is:' + str([''.join(map(str, vectors[i])) for i in optimalVectorIndices]))
if BENCHMARK:
    critical_outputs.append('\n\n\t\t\t=======>OVERALL DURATION: ' + str(datetime.now() - timer) + '===============\n\n')
    detailed_outputs.append(critical_outputs[-1])
file = None
if FIO:
    file = open("acktraqdisovery.txt", "w")
for line in detailed_outputs:
    if PIO:
        print(line)
    if FIO:
        file.write(line)
        file.write('\n')
if not PIO:
    for line in critical_outputs:
        print(line)
if FIO:
    file.close()
