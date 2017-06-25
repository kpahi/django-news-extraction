import os
import subprocess
from subprocess import PIPE, Popen, check_call

import nltk
from nltk import conlltags2tree, tree2conlltags
from nltk.tree import Tree

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(DIR, 'extraction')
script = path + '/us.py'
#
# sentence = 'Two pedestrians were fatally hit by vehicles in assorted locations of Kathmandu valley on Thursday, police said.'
# command = './us.py {0}'.format(sentence)

# open process us.py with sentence as input
sentence = "A biker died after being hit by a tractor at Sundar Haraicha Municipality-12 in Morang district along the East-West Highway on Sunday."


# tree parsing
def geotraverseTree(sentence):
    # sentence = 'Two pedestrians were fatally hit by vehicles in assorted locations of Kathmandu valley on Thursday, police said.'
    """The deceased has been identified as Shyam Karki, 32, of Kerabari Rural Municipality-9 of the district."""
    print(sentence)
    p = subprocess.Popen([script, sentence], stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    print(stdout)
    output = stdout.decode('ascii')
    print(output)

    # transform string type output into nltk tree
    t = nltk.tree.Tree.fromstring(output)
    leaf = []
    for subtree in t:
        if type(subtree) == nltk.tree.Tree:
            if(subtree.label() == "geo"):  # extract geo marked subtree
                leaf = ''.join(subtree.leaves())
                lst = leaf.split("/")
    return lst[0]

if __name__ == "__main__":
    x = geotraverseTree(sentence)
    print(x)
# print(traverseTree(t))
