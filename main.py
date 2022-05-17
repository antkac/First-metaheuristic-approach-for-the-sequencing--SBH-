import generator
import graph
import comparison
import itertools as tools
from collections import OrderedDict
from functools import reduce
import random
import time


def Average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)


def stick_together(a, b):
    return max(i for i in range(len(b) + 1) if a.endswith(b[:i]))


def overlap(permutation, k):
    count = 1
    res = permutation[0]
    for s in permutation[1:]:
        o = stick_together(res, s)
        if(o!=0):
            count+=1
            res += s[o:]
    # permutation_list.append(res)
    # permutation_nuc_count.append(count)
    return  res , count
    print(f'{res} used:{count}')


original_length = 100
original_k = 8
n_permutations = 100000

avg_fitness = []

population_n = 300
generations_n = 40

permutation_list = list()
permutation_nuc_list = list()
permutation_nuc_count = list()
permutation_fitness = list()

next_gen_nuc = list()
next_gen_fitness = list()


start = time.time()


##### Primary Generation #####
print("working...")        # Tu w wywolaniu mozna podac zadane wartosci np. (120,9,3,0.9,0.1)    albo standardowe sie uruchomia (length=100, k=7, p=5, per_p=0.5, per_n=0.5)
subseq_lst = generator.generate(length=original_length, k=original_k)   # length - dlugosc sekwencji    k - dlugosc podciagow    p - procent bledow    per_p - procent bledow poz  per_n - procent bledow neg
# print(subseq_lst)

subseq_dict = generator.subseq_count(subseq_lst)      # Utworzenie słownika gdzie item to podciag a value to ilosc wystapien w sekwencji
# print(subseq_dict)

subseq_lst = list(OrderedDict.fromkeys(subseq_lst))   # removing duplicate subsequences from list
random.shuffle(subseq_lst)
# print(subseq_lst)
##### END #####


#----------------------------------------------------------------------------------------------------------------------#
'''G = graph.defaultdict(list)
for pair in tools.permutations(subseq_lst, 2):  # lista sasiedztwa
    # print(pair[0],pair[1])
    graph.add_egde(G, pair[0], pair[1])
print(G)'''
#----------------------------------------------------------------------------------------------------------------------#


##### Permutations and Fitness #####
for permutation in tools.islice(tools.permutations(subseq_lst),0,n_permutations):
    # x=list(permutation)
    # x=random.shuffle(x)
    # permutation_nuc_list.append(x)
    permutation_nuc_list.append(permutation)
    # print(f'permutacja: {permutation}')
    res, count = overlap(permutation, original_k)               # Check overlaping and num of used elements from spectrum
    permutation_list.append(res)
    permutation_nuc_count.append(count)

for org in permutation_nuc_count:                  # Calculating fitness
    fitness = comparison.fitness(org,original_length,original_k)
    permutation_fitness.append(fitness)
    # print(f'org {org} fitness: {fitness}')
##### END #####


avg_fitness.append(Average(permutation_fitness))   # Primary population avg fitness


##### Printing #####
# only for testing
'''
print("permutation list:")
print(permutation_list)
print(permutation_nuc_count)
print(permutation_fitness)
'''
##### END #####




for generations in range(generations_n):
    print(f"working...  gen[{generations+1}] ")


    ##### Tournament #####
    population = 0
    while len(next_gen_nuc) < population_n:   # desired population of parents size 300 tournament of 8
        selected_list = list()
        selected_fitness = list()
        for i in range(8):
            x = random.randrange(len(permutation_nuc_list))
            selected_list.append(permutation_nuc_list[x])
            selected_fitness.append(permutation_fitness[x])
        winner, winner_score = comparison.tournament(selected_list,selected_fitness)
        next_gen_nuc.append(list(winner))
        next_gen_fitness.append(winner_score)
        population+=1
        # print(f'\nwinner: {population}\n{winner}\nscore:\n{winner_score}')
    ##### END #####


    ##### Crossing-Over #####
    for one, two in grouped(next_gen_nuc,2):            # Crossover
        # print(f'one : {one}')
        # print(f'two : {two}')
        choices = ['single', 'multi', 'none']
        choice = random.choices(choices, weights=[0.5,0.4,0.1])[0]
        if choice == 'single':
            child1, child2 = comparison.single_crossover(one,two)
            child1 = child1.tolist()
            child2 = child2.tolist()
            next_gen_nuc.append(child1)
            res, score = overlap(child1,original_k)
            next_gen_fitness.append(comparison.fitness(score,original_length,original_k))
            next_gen_nuc.append(child2)
            res, score = overlap(child2, original_k)
            next_gen_fitness.append(comparison.fitness(score,original_length,original_k))
            #print(f' s SCOOOOOOOOOOOOORE : {comparison.fitness(score,original_length,original_k)}')
            # print(child1.tolist())
            # print(child2.tolist())
        if choice == 'multi':
            child1, child2 = comparison.multi_crossover(one,two)
            child1 = child1.tolist()
            child2 = child2.tolist()
            next_gen_nuc.append(child1)
            res, score = overlap(child1, original_k)
            next_gen_fitness.append(comparison.fitness(score,original_length,original_k))
            next_gen_nuc.append(child2)
            res, score = overlap(child2, original_k)
            next_gen_fitness.append(comparison.fitness(score,original_length,original_k))
            #print(f' m SCOOOOOOOOOOOOORE : {comparison.fitness(score,original_length,original_k)}')
            # print(child1.tolist())
            # print(child2.tolist())
        if choice == 'none':
            #print("no crossing over !!!!!!!!!!!!!!!")
            pass
    # print(f'size :  {len(next_gen_nuc)}')
    avg_fitness.append(Average(next_gen_fitness))
    print(Average(next_gen_fitness))
    ##### END  #####


    # print(avg_fitness)


    ##### Mutate  #####
    comparison.mutation(next_gen_nuc)
    next_gen_fitness.clear()

    for org in next_gen_nuc:                  # Calculating fitness
        res, score = overlap(org, original_k)
        next_gen_fitness.append(comparison.fitness(score, original_length, original_k))
    avg_fitness.append(Average(next_gen_fitness))
    ##### END  #####



    ##### Eliminate excess  #####
    tmp_lst= []
    for seq, score in zip(next_gen_nuc,next_gen_fitness):
        tmp_lst.append([seq,score])
    tmp_lst.sort(key=lambda row: row[1], reverse= True)
    next_gen_nuc.clear()
    next_gen_fitness.clear()
    permutation_nuc_list.clear()
    permutation_fitness.clear()
    while len(permutation_nuc_list) < population_n:
        queue = 0
        permutation_nuc_list.append(tmp_lst[0][0])
        permutation_fitness.append(tmp_lst[0][1])
        queue += 1
    ##### END  #####

print(f'Primary population fitness: {avg_fitness[0]}')


print(f'\nBest avg score: {max(avg_fitness)}')
end = time.time()
print("\n--- %s seconds ---" % (end - start))
