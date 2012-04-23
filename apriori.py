import sys
import os.path
import csv
import math 
from collections import defaultdict
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

        self.F[1] = self.firstPass(self.itemset, 1)
        print "First Pass: "
        print self.F[1]
        k=2
        candidate[k] = self.candidateGen(self.F[k-1], k-1)
        #print "Candidate[k]: "
        #print candidate[k]
        while len(self.F[k-1]) != 0:
            candidate[k] = self.candidateGen(self.F[k-1], k-1)
            print candidate[k]
            for c in candidate[k]:
                count[frozenset(c)] = 0
            for t in self.transList.iteritems():
                for c in candidate[k]:
                    if set(c).issubset(t[1]):
                        count[frozenset(c)] += 1

            self.F[k] = self.prune(candidate[k], count, k)
            print self.F[k]
            k += 1

        for row in self.F.items():
            print row

    def hasSubset(self, c, t):
        flag = False
        for item in c:
            flag = item in t[1]

        return flag

    def frozenSupport(self, counts, item):
        return float(counts[frozenset(item)])/self.numItems

    def support(self, item):
        return float(self.freqList[int(item)])/self.numItems

    #def frequency(self, item):
    #    return float(self.freqList[item])/

    def prune(self, items, counts, k):
        f = []
        for item in items:
            support = self.frozenSupport(counts, item)
            if support >= self.minSup:
                f.append(item)

        return f

    def firstPass(self, items, k):
        f = []
        for item in items:
            support = self.support(item)
            if support >= self.minSup:
                f.append(item)

        return f

    def candidateGen(self, items, k):
        candidate = []

        if len(items) > 2:
            for f1, f2 in itertools.combinations(items, 2):
                c = [f1, f2]
                candidate.append(c)

        return candidate

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
                    self.transList[key].append(int(item))
                    self.itemset.add(int(item))
                    self.freqList[int(item)] += 1

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
