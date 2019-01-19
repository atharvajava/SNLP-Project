from nltk.parse import CoreNLPParser
from nltk.tree import *

parser = CoreNLPParser(url='http://localhost:9000')
ls=list(parser.parse("Alfonso XIII of Spain's birth place is Madrid.".split()))
ls=ParentedTree.fromstring(str(ls[0]))

def getSubject(t):
    for s in t.subtrees(lambda t: t.label() == 'NP'):
        for n in s.subtrees(lambda n: n.label().startswith('NN')):
            return(n[0],getAttributes(n))

def getPredicate(t):    
    v = None
    
    for s in t.subtrees(lambda t: t.label() == 'VP'):
        for n in s.subtrees(lambda n: n.label().startswith('VB')):
            v = n
            return(v[0], getAttributes(v))

def getObject(t):    
    for s in t.subtrees(lambda t: t.label() == 'VP'):
        for n in s.subtrees(lambda n: n.label() in ['NP', 'PP', 'ADJP']):
            if n.label() in ['NP', 'PP']:
                for c in n.subtrees(lambda c: c.label().startswith('NN')):
                    return(c[0], getAttributes(c))
            else:
                for c in n.subtrees(lambda c: c.label().startswith('JJ')):
                    return(c[0], getAttributes(c))

def getAttributes(node):
    attrs = []
    p = node.parent()

    # Searching Siblings
    if node.label().startswith('JJ'):
        for s in p:
            if s.label() == 'RB':
                attrs.append(s[0])
        
    elif node.label().startswith('NN'):
        for s in p:
            if s.label() in ['DT','PRP$','POS','JJ','CD','ADJP','QP','NP']:
                attrs.append(' '.join(s.flatten()))

    elif node.label().startswith('VB'):
        for s in p:
            if s.label() == 'ADVP':
                attrs.append(' '.join(s.flatten()))

    if node.label().startswith('JJ') or node.label().startswith('NN'):
        for s in p.parent():
            if s != p and s.label() == 'PP':
                attrs.append(' '.join(s.flatten()))

    elif node.label().startswith('VB'):
        for s in p.parent():
            if s != p and s.label().startswith('VB'):
                attrs.append(s[0])

    return attrs




print(getSubject(ls[0]))