import os
import subprocess
from subprocess import PIPE, Popen, check_call

import nltk
from nltk import conlltags2tree, tree2conlltags
from nltk.tree import Tree

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(DIR, 'extraction')
print(path)
script = path + '/us.py'
print(script)
#
# sentence = 'Two pedestrians were fatally hit by vehicles in assorted locations of Kathmandu valley on Thursday, police said.'
# command = './us.py {0}'.format(sentence)

# open process us.py with sentence as input
sentence = "A biker died after being hit by a tractor at Sundar Haraicha Municipality-12 in Morang district along the East-West Highway on Sunday."

#sentence = "Jun 22, 2017-A person died and four others were injured when a micro bus hit them at Jorpati, Kathmandu on Thursday."


# tree parsing


def geotraverseTree(sentence):
    # sentence = 'Two pedestrians were fatally hit by vehicles in assorted locations of Kathmandu valley on Thursday, police said.'
    # """The deceased has been identified as Shyam Karki, 32, of Kerabari Rural Municipality-9 of the district."""
    # print(sentence)
    p = subprocess.Popen([script, sentence], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    # print("Outpute after subprocess")
    # print(stdout)
    output = stdout.decode('ascii')
    # print(output)

    # transform string type output into nltk tree
    t = nltk.tree.Tree.fromstring(output)
    leaf = []
    lst= []
    for subtree in t:
        if type(subtree) == nltk.tree.Tree:
            if(subtree.label() == "geo"):  # extract geo marked subtree
                leaf = ''.join(subtree.leaves())
                lst = leaf.split("/")
    if not lst:
        loc = "None"
    else:
        loc = lst[0]
    # print(loc)
    # print("The Extracted location {}".format(lst[0]))
    return loc

if __name__ == "__main__":
    x = geotraverseTree(sentence)
    print(x)
# print(traverseTree(t))
