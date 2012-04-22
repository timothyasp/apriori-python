import sys
import os.path
import csv
import math 
from collections import defaultdict
import itertools

class Apriori:
    def __init__(self, data, minSup, minConf):
        self.dataset = data
        self.transactions = defaultdict(set)
        self.freqList = defaultdict(int)
        self.itemset = set()
        self.prepData() # initialize the above collections

        self.F = defaultdict(list) # frequent itemset

        self.minSup = minSup
        self.minConf = minConf

    def genAssociations(self):
        #self.F[1] = self._firstPass()
        count = defaultdict(int)
        self.minsupSubset(1, self.freqList.items())
        C = {}

        k=2
        #while self.F[k-1] != set():
        C[k] = self.candidateGen(self.F[k-1], k-1)

            #for row in C[k]:
            #    count[row] = 0

            #for t in self.transactions:
            #    for c in C[k]:
            #        if c.issubset(t):
            #            count[c]++

            #minsupSubset(k, C[k])
        #    k += 1

    def support(self, item):
        return float(self.freqList[int(item[0])])/len(self.transactions.items())

    def minsupSubset(self, k, c):
        for item in c:
            if self.support(item) >= self.minSup:
                self.F[k].append(item[0])

    def candidateGen(self, F, k):
        C = set()
        print F

        print set([i.union(j) for i in F for j in F if len(i.union(j)) == k])
        for element in itertools.product(F, F):
            print element

        

        #print [(i, j) for i in F for j in F]

    """
    Prepare the transaction data into a dictionary
    key: Receipt.id
    val: set(Goods.Id) 

    Also generates the frequent itemlist for itemsets of size 1
    key: Goods.Id
    val: frequency of Goods.Id in self.transactions
    """
    def prepData(self):
        for v in self.dataset:
            k = v[0] # key is Goods.id
            for i, val in enumerate(v):
                if i != 0:
                    self.freqList[int(val)] += 1
                    self.transactions[int(k)].add(val)

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
