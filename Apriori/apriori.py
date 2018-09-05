with open('Data.txt') as f:
    data = [line.strip().replace(" ", "").split(',') for line in f]

parameter = data.pop(0)
min_sup = float(parameter[0]); out_r = float(parameter[1])


def getSupport(Data, candidates):
    support = []
    for candidate in candidates:
        count = 0
        for record in Data:
            exist = True
            for item in candidate:
                if item not in record:
                    exist = False
            if exist:
                count+=1
        support.append(count)
    return support


def pruneCandidate(candidates, support, min_sup, number):
    indexes = []
    for i,candidate in enumerate(candidates):
        if float(support[i])/number < min_sup:
            indexes.append(i)
    for index in sorted(indexes,reverse=True):
        candidates.pop(index)
    return candidates


def nextCandidates(candidates):
    next_can = []
    for candidate1 in candidates:
        for candidate2 in candidates:
            if(candidate2 != candidate1):
                combine = []
                for item in candidate1:
                    if item not in combine:
                        combine.append(item)
                for item in candidate2:
                    if item not in combine:
                        combine.append(item)
                combine.sort()
                if combine not in next_can:
                    if len(combine) == len(candidate1)+1:
                        next_can.append(combine)
    return next_can


def apriori(Data, min_sup):
    number = len(Data)
    C1 = {}
    for record in Data:
        record = list(set(record))
        for item in record:
            if item in C1:
                C1[item] += 1
            else:
                C1[item] = 1
    _keys1 = C1.keys()
    keys1 = []
    for i in _keys1:
        keys1.append([i])
    F1 = []
    for i in keys1[:]:
        if float(C1[i[0]])/number >= min_sup:
            F1.append(i)
    F1.sort()
    candidates = F1
    all_freqs = []
    while candidates != []:
        sup = getSupport(Data,candidates)
        freq = pruneCandidate(candidates,sup,min_sup,number)
        for sets in freq:
            all_freqs.append(sets)
        candidates = nextCandidates(freq)
    return all_freqs


F = apriori(data, min_sup)
print '\nfrequent itemset:\n', F

'''
number = len(data)
C1 = {}
for record in data:
    record = list(set(record))
    for item in record:
        if item in C1:
            C1[item] += 1
        else:
            C1[item] = 1
_keys1 = C1.keys()
keys1 = []
for i in _keys1:
    keys1.append([i])
F1 = []
for i in keys1[:]:
    if float(C1[i[0]])/number >= min_sup:
        F1.append(i)

F1.sort()
candidates = F1
sup = getSupport(data,candidates)
freq = pruneCandidate(candidates,sup,min_sup,number)

candidates = nextCandidates(freq)
candidates_c = candidates[:]
sup = getSupport(data,candidates)
freq = pruneCandidate(candidates,sup,min_sup,number)

candidates = nextCandidates(freq)
candidates_c = candidates[:]
sup = getSupport(data,candidates)
freq = pruneCandidate(candidates,sup,min_sup,number)

candidates = nextCandidates(freq)
candidates_c = candidates[:]
sup = getSupport(data,candidates)
freq = pruneCandidate(candidates,sup,min_sup,number)

print(candidates_c)
print(sup)
print(freq)
'''