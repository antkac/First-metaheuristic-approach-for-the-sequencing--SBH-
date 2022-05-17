import random


def generate_subseq(k):     # k - substing length
    return ''.join(random.choice('CGTA') for _ in range(k))


def splice(seq, k):
    for i in range((len(seq)-(k-1))):
        yield seq[i:k+i]


def mutate(lst, k, p, per_p, per_n):     # positive and negative signals simulation
    choices = ['P', 'N']
    n_mutation = (len(lst)*p)//100
    for mutation in range(n_mutation):
        type_of_mutation = random.choices(choices, weights=(per_p, per_n))
        if(''.join(type_of_mutation) == 'P'):  # positive signals
            added = False
            while(added is not True):
                subseq = generate_subseq(k)
                if(generate_subseq(k) not in lst):
                    lst.append(subseq)
                    added = True
        elif(''.join(type_of_mutation) == 'N'):  # negative signals
            x = random.choice(lst)
            lst.remove(x)


def generate(length=100, k=7, p=5, per_p=0.5, per_n=0.5):  # length - dlugosc sekwencji    k - dlugosc podciagow    p - procent bledow    per_p - procent bledow poz  per_n - procent bledow neg
    lst = list()
    seq = ''.join(random.choice('CGTA') for _ in range(length))
    # print(seq)
    for substrings in splice(seq, k):
        lst.append(substrings)
    mutate(lst, k, p, per_p, per_n)
    return lst


def subseq_count(lst):   # count occurances of subsequences
    d = {}
    for subseq in lst:
        if subseq not in d:
            d[subseq] = 0
        d[subseq] += 1
    return d
