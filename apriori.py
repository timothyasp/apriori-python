import sys
import os.path
import csv
import math 
import types
from collections import defaultdict, Iterable
import itertools

class Apriori:
    def __init__(self, data, minSup, minConf):
        self.dataset = data
        self.transList = defaultdict(list)
        self.freqList = defaultdict(int)
        self.itemset = set()
        self.numItems = 0
        self.prepData()             # initialize the above collections

        self.F = defaultdict(list)

        self.minSup = minSup
        self.minConf = minConf

    def genAssociations(self):
        candidate = {}
        count = {}

        self.F[1] = self.firstPass(self.freqList, 1)
        k=2
        while len(self.F[k-1]) != 0:
            candidate[k] = set(self.candidateGen(self.F[k-1], k))
            for t in self.transList.iteritems():
                for c in candidate[k]:
                    if set(c).issubset(t[1]):
                        self.freqList[c] += 1

            self.F[k] = self.prune(candidate[k], k)
            k += 1

        self.genRules(self.F, self.minConf)

    def prune(self, items, k):
        f = []
        for item in items:
            count = self.freqList[item]
            if self.support(count) >= self.minSup:
                f.append(item)

        return f

    def isSubset(self, c, t):
        cSize = len(c)
        size = 0
        for x in c:
            for y in t:
                if x == y:
                    size += 1
        return size == cSize

    def candidateGen(self, items, k):
        candidate = []

        for c in itertools.combinations(items, k):
            if k > 2:
                itemset = set()
                for x in c:
                    itemset = set(x).union(itemset)
                    if len(itemset) == k:
                        candidate.append(tuple(itemset))
            else:
                flag = True
                for s in c:
                    if s not in items:
                        flag = False
                if flag:
                    candidate.append(c)

        return candidate

    def genRules(self, F, minConf):
        H = []
        for k, itemset in F.iteritems():
            for item in itemset:
                if k >= 2:
                    subsets = self.genSubsets(item)
                    for subset in subsets:
                        if len(subset) == 1:
                            subCount = self.freqList[subset[0]]
                        else:
                            subCount = self.freqList[subset]
                        itemCount = self.freqList[item]
                        if subCount != 0:
                            confidence = self.confidence(subCount, itemCount)
                            if confidence >= self.minConf:
                                support = self.support(self.freqList[item])
                                rhs = self.difference(item, subset)
                                if len(rhs) == 1:
                                    H.append((subset, rhs, support, confidence))

        self.skylineRules(H)

    def skylineRules(self, H):
        for rule in H:
            print rule

    def difference(self, item, subset):
        return tuple(x for x in item if x not in subset)

    def confidence(self, subCount, itemCount):
        return float(itemCount)/subCount

    def support(self, count):
        return float(count)/self.numItems

    def genSubsets(self, item):
        subsets = []
        length = len(item)
        for i in range(1,length):
            combs = itertools.combinations(item, i)
            subsets.extend(combs)
        return subsets

    def firstPass(self, items, k):
        f = []
        for item, count in items.iteritems():
            if self.support(count) >= self.minSup:
                f.append(item)

        return f

    """
    Prepare the transaction data into a dictionary
    key: Receipt.id
    val: set(Goods.Id) 

    Also generates the frequent itemlist for itemsets of size 1
    key: Goods.Id
    val: frequency of Goods.Id in self.transList
    """
    def prepData(self):
        key = 0
        for basket in self.dataset:
            self.numItems += 1
            key = basket[0]
            for i, item in enumerate(basket):
                if i != 0:
                    self.transList[key].append(item.strip())
                    self.itemset.add(item.strip())
                    self.freqList[(item.strip())] += 1

def main():
    num_args = len(sys.argv)
    minSup = minConf = 0

    # Make sure the right number of input files are specified
    if  num_args != 4:
        print 'Expected input format: python apriori.py <dataset.csv> <minSup> <minConf>'
        return
    # If they are read them in
    else: 
        dataset = csv.reader(open(sys.argv[1], "r"))
        minSup  = float(sys.argv[2])
        minConf = float(sys.argv[3])

        a = Apriori(dataset, minSup, minConf)

        a.genAssociations()


if __name__ == '__main__':
    main()
