from collections import Counter
from itertools import combinations

support = 0
while True:
    support = int(input("Please enter a number for the support: "))
    if support > 0:
        break


"""
Returns baskets --> a list of all the baskets
"""
def ReadBaskets():

    infile = ('T10I4D100K.dat')
    baskets = []

    with open(infile, 'r') as file:
        for transaction in file:
            j = transaction.rstrip().split(" ")
            basket = []
            for item in j:
                item = int(item)
                basket.append(item)
            baskets.append(basket)

    return baskets

baskets = ReadBaskets()

"""
 Returns items_with_support --> dictionary with key = item and value = # of occurrences, i.e. {25: 522}
"""
def CreateItemsWithSupport(baskets, support):
    items_with_support = Counter(x for xs in baskets for x in set(xs))

    for key in list(items_with_support):
        if items_with_support[key] < support:
            del items_with_support[key]
    return items_with_support

items_with_support = CreateItemsWithSupport(baskets, support)

"""
Creates the L1 set, set of the frequent singletons
"""
def CreateL1(items_with_support):
    L1 = set([])
    for key in items_with_support:
        L1.add(key)
    return L1

L1 = CreateL1(items_with_support)

"""
Creates the Ck -> list of all possible combinations from Lk_1 and uses its elements
to check if they are frequent.
"""
def getLk(Lk_1, baskets, support, k):
    Lk = {}
    tempList = []
    for basket in baskets:
        bask = list(L1.intersection(basket))
        bask.sort()
        Ck = list(combinations(bask, k))

        for tuple in Ck:
            if checkToAdd(tuple, Lk_1, k):
                if tuple in Lk:
                    Lk[tuple] += 1
                else:
                    Lk[tuple] = 1

    for tuple in list(Lk):
        if Lk[tuple] < support:
            del Lk[tuple]

    return Lk

"""
Performs a check if the tuples from Ck exist in Lk_1.
"""
def checkToAdd(tuples, Lk_1, k):
    combs = combinations(list(tuples), k - 1)
    for tuple in combs:
        if (len(tuple) == 1):
            if tuple[0] not in Lk_1:
                return False
            else:
                return True
        elif (len(tuple) > 1):
            if tuple not in Lk_1:
                return False
            else:
                return True



def Apriori(L1, baskets, support):
    k = 2
    Lk = L1
    resultSet = []
    while(len(Lk) > 0):
        resultSet.append(Lk)
        Lk = getLk(Lk, baskets, support, k)
        k += 1
    print(resultSet)    
    return resultSet


def Calling(L1, baskets, support):
    results = Apriori(L1, baskets, support)
    for i in range (len(results)):
	       print ("Number of itemsets with length " + str(i + 1) +": " + str(len(results[i])))

Calling(L1, baskets, support)
