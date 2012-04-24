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
        #print "First Pass: "
        #print self.F[1]
        k=2
        #print "Candidate[k]: "
        #print candidate[k]
        while len(self.F[k-1]) != 0:
            candidate[k] = self.candidateGen(self.F[k-1], k-1)
            #print candidate[k]
            #for c in candidate[k]:
            #    count[frozenset(c)] = 0
            for t in self.transList.iteritems():
                for c in candidate[k]:
                    if self.isSubset(c, t[1]):
                        self.freqList[c] += 1

            self.F[k] = self.prune(candidate[k], k)
            k += 1

        self.genRules(self.F, self.minConf)

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

        for f1, f2 in itertools.combinations(items, 2):
            c = (f1, f2)
            if len(c) == k+1:
                flag = True
                for s in c:
                    if s not in items:
                        flag = False
                if flag:
                    candidate.append(c)

        return candidate

    def genRules(self, F, minConf):
        for k, itemset in F.iteritems():
            H = []
            print itemset
            for item in itemset:
                if k >= 2:
                    subsets = self.genSubsets(item)
                    for subset in subsets:
                        subCount = self.freqList[subset[0]]
                        itemCount = self.freqList[item]
                        confidence = self.confidence(subCount, itemCount)
                        if confidence >= self.minConf:
                            support = self.support(self.freqList[item])
                            print subset, self.difference(item, subset), support, confidence

    def difference(self, item, subset):
        return tuple(x for x in item if x not in subset)

    def confidence(self, subCount, itemCount):
        return float(itemCount)/subCount

    def genSubsets(self, item):
        subsets = []
        length = len(item)
        for i in range(1,length):
            subsets.extend(itertools.combinations(item, i))
        return subsets

    def frozenSupport(self, counts, item):
        return float(counts[frozenset(item)])/self.numItems

    def support(self, count):
        return float(count)/self.numItems

    def prune(self, items, k):
        f = []
        for item in items:
            count = self.freqList[item]
            if self.support(count) >= self.minSup:
                f.append(item)

        return f

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
                    self.transList[key].append(item)
                    self.itemset.add(item)
                    self.freqList[(item)] += 1

#def genRules(F, minConf):

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
