import csv
import nltk
import wikipedia

class FactCheck:
    trainData=[]

    def function(self):
        print("This is a message inside the class.")

    def train(self):
        with open("train.tsv", encoding="ISO-8859-1") as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                self.trainData.append(row)
                tokens=nltk.word_tokenize(row["Fact_Statement"])
                tagged = nltk.pos_tag(tokens)

    def levenshteinDistance(self,s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]

    def wiki(self):
        s1="Adolphe Thiers' office is France."
        listofpage=wikipedia.search(s1)
        dist=len(s1)
        pagetag=""
        for s2 in listofpage:
            tempdis=self.levenshteinDistance(s1,s2)
            print(s2 + " "+ str(tempdis))
            if tempdis < dist:
                print(tempdis)
                dist=tempdis
                pagetag=s2
        print(listofpage)
        print(pagetag)

                

from nltk.parse import CoreNLPParser
from nltk.tree import *

parser = CoreNLPParser(url='http://localhost:9000')
ls=list(parser.parse('What is the airspeed of an unladen swallow ?'.split()))

for s in ls[0].subtrees(lambda t: t.label() == 'NP'):
    for n in s.subtrees(lambda n: n.label().startswith('NN')):
        print(n[0])
