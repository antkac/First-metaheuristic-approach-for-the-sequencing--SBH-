import numpy as np
import random

def hamming_distance(seq1, seq2):
    return sum([1 for n1, n2 in zip(seq1, seq2) if n1 != n2])
    # not used


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1
                )
    return matrix[size_x - 1, size_y - 1]
    # not used


def fitness(used, n, k):  # seq composed of the most elements from spectrum, length not greater than n nucleotides
    expected_used = n-k+1
    result = used/expected_used
    return result


def random_crossover(a, b):
    p = np.random.rand(len(a))
    for i in range(len(p)):
        if p[i] < 0.5:
            a[i] = b[i]
    return a


def single_crossover(a, b,x=0):
    # print('single')
    if x == 0:
        x = int(0.25 * len(a))
    new1 = np.append(a[:x], b[x:])
    new2 = np.append(b[:x], a[x:])
    return new1, new2


def multi_crossover(a,b):
    # print('multi')
    x = np.array([2,(0.9*len(a))])
    for i in x:
        a, b = single_crossover(a, b, int(i))
    return a, b


def tournament(list_of_candidats, list_of_scores):
        best_fitness = max(list_of_scores)
        max_index = list_of_scores.index(best_fitness)
        winner = list_of_candidats[max_index]
        return winner, best_fitness


def mutation(lst,p=10):
    n_mutation = int((len(lst) * p) // 100)
    n_mutation2 = int((len(lst) * 5) // 100)
    choices = ['Del', 'Ins', 'Sub']
    for mutation in range(n_mutation):
        random_seq = random.randrange(len(lst))
        chosen_seq = lst[random_seq]
        for mutation2 in range(n_mutation2):
            random_oligo = random.randrange(len(chosen_seq)-1)
            chosen_oligo = list(lst[random_oligo])
            type_of_mutation = random.choice(choices)

            if type_of_mutation == "Del":
                chosen_oligo = list(lst[random_seq][random_oligo].strip(" "))
                if len(chosen_oligo) > 2:
                    random_nuc = random.randrange(0,len(chosen_oligo)-1)
                    del chosen_oligo[random_nuc]
                    lst[random_seq][random_oligo] = ''.join(chosen_oligo)
            if type_of_mutation == "Ins":
                add = random.choice(["C", "A", "G", "T"])
                chosen_oligo = list(lst[random_seq][random_oligo].strip(" "))
                chosen_oligo.append(add)
                lst[random_seq][random_oligo] = ''.join(chosen_oligo)
            if type_of_mutation == "Sub":
                sub = random.choice(["C", "A", "G", "T"])
                chosen_oligo = list(lst[random_seq][random_oligo].strip(" "))
                if len(chosen_oligo) > 2:
                    random_nuc = random.randrange(0,len(chosen_oligo)-1)
                    #print(f'{chosen_oligo}')
                    chosen_oligo[random_nuc] = sub
                    # print(f'{chosen_oligo}')
        #lst[random_oligo] = cos

