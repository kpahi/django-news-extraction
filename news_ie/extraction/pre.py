import collections
import itertools
import os
import os.path
import pickle
import re
import string
import sys

import numpy as np
from nltk import conlltags2tree, pos_tag, tree2conlltags, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

stemmer = SnowballStemmer('english')

# from read_data import features

# vectorizer = DictVectorizer(sparse=False)


def features(tokens, index, history):
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    `history` = the previous predicted IOB tags
    """

    # init the stemmer

    # Pad the sequence with placeholders
    tokens = [('[START2]', '[START2]'), ('[START1]', '[START1]')] + \
        list(tokens) + [('[END1]', '[END1]'), ('[END2]', '[END2]')]
    history = ['[START2]', '[START1]'] + list(history)

    # shift the index with 2, to accommodate the padding
    index += 2

    word, pos = tokens[index]
    prevword, prevpos = tokens[index - 1]
    prevprevword, prevprevpos = tokens[index - 2]
    nextword, nextpos = tokens[index + 1]
    nextnextword, nextnextpos = tokens[index + 2]
    previob = history[-1]
    prevpreviob = history[-2]

    feat_dict = {
        'word': word,
        'lemma': stemmer.stem(word),
        'pos': pos,
        'shape': shape(word),

        'next-word': nextword,
        'next-pos': nextpos,
        'next-lemma': stemmer.stem(nextword),
        'next-shape': shape(nextword),

        'next-next-word': nextnextword,
        'next-next-pos': nextnextpos,
        'next-next-lemma': stemmer.stem(nextnextword),
        'next-next-shape': shape(nextnextword),

        'prev-word': prevword,
        'prev-pos': prevpos,
        'prev-lemma': stemmer.stem(prevword),
        'prev-iob': previob,
        'prev-shape': shape(prevword),

        'prev-prev-word': prevprevword,
        'prev-prev-pos': prevprevpos,
        'prev-prev-lemma': stemmer.stem(prevprevword),
        'prev-prev-iob': prevpreviob,
        'prev-prev-shape': shape(prevprevword),
    }

    return feat_dict


def shape(word):
    word_shape = 'other'
    if re.match('[0-9]+(\.[0-9]*)?|[0-9]*\.[0-9]+$', word):
        word_shape = 'number'
    elif re.match('\W+$', word):
        word_shape = 'punct'
    elif re.match('[A-Z][a-z]+$', word):
        word_shape = 'capitalized'
    elif re.match('[A-Z]+$', word):
        word_shape = 'uppercase'
    elif re.match('[a-z]+$', word):
        word_shape = 'lowercase'
    elif re.match('[A-Z][a-z]+[A-Z][a-z]+[A-Za-z]*$', word):
        word_shape = 'camelcase'
    elif re.match('[A-Za-z]+$', word):
        word_shape = 'mixedcase'
    elif re.match('__.+__$', word):
        word_shape = 'wildcard'
    elif re.match('[A-Za-z0-9]+\.$', word):
        word_shape = 'ending-dot'
    elif re.match('[A-Za-z0-9]+\.[A-Za-z0-9\.]+\.$', word):
        word_shape = 'abbreviation'
    elif re.match('[A-Za-z0-9]+\-[A-Za-z0-9\-]+.*$', word):
        word_shape = 'contains-hyphen'

    return word_shape



def ner(sentence):

    # load the model from disk
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(DIR, 'extraction')

    vectorizer = joblib.load(os.path.join(path,'vectorizer.pkl'))
    ppn = joblib.load(os.path.join(path,'ppn.pkl'))

    # filename = 'vec_and_ppn.pkl'
    # loaded_model = joblib.load(filename)
    # vec, ppn = loaded_model['vectorizer'], loaded_model['ppn']

    # vectorizer = pickle.load(open("vectorizer.pickle"))

    print("Model load done")
    print("Predicting new sentences:")

    new = pos_tag(word_tokenize(sentence))
    #    "A man has died in a road accident that took place at Urlabari - 3 on the East - West highway on Saturday evening."))
    # "DHARAN, July 23: There are potholes everywhere in a one-kilometer road stretch of Koshi Highway that runs through Dharan."))
    # "A person died and four others were injured when a micro bus hit them at Jorpati, Kathmandu on Thursday."))


    history = []
    iob_tagged_tokens = []
    for index, (word, tag) in enumerate(new):
        f = features(new, index, history)
        new_transform = vectorizer.transform(f)
        ner_tag = ppn.predict(new_transform)
        # print("Predicted NER TAG for current")
        # print(word, "Corresponding Tokens", ner_tag[0])
        # print(ppn.predict(new_transform))

        iob_tag = ner_tag[0]
        history.append(iob_tag)
        # print(iob_tag)
        # print("\n")
        # print("Predict current one\n")
        #
        #
        # new_transform = vectorizer.transform(iob_tag)
        # print(ppn.predict(new_transform))

        iob_tagged_tokens.append((word, tag, iob_tag))
    return iob_tagged_tokens

    # print(ready)

    # print(iob_tagged_tokens)
# sent = "A man has died in a road accident that took place at Urlabari - 3 on the East - West highway on Saturday evening."
# print(ner(sent))
