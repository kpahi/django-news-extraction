import collections
import os
import os.path
import re
import string
import sys

from nltk import conlltags2tree, tree2conlltags
from nltk.stem.snowball import SnowballStemmer

ner_tags = collections.Counter()

basepath = os.path.dirname(__file__)
corpus_root = os.path.abspath(os.path.join(basepath, "gmb-2.2.0"))

# corpus_root = "gmb-2.2.0.zip"
# reload(sys)
# sys.setdefaultencoding('utf-8')


def read_gmb(corpus_root):
    for root, dirs, files in os.walk(corpus_root):
        for filename in files:
            if filename.endswith(".tags"):
                with open(os.path.join(root, filename), 'rb') as file_handle:
                    # file_handle = zipfile.ZipFile('gmb-2.2.0.zip', 'r')
                    file_content = file_handle.read().decode('utf-8').strip()
                    annotated_sentences = file_content.split('\n\n')
                    for annotated_sentence in annotated_sentences:
                        annotated_tokens = [seq for seq in annotated_sentence.split('\n') if seq]
                        standard_form_tokens = []
                        for idx, annotated_token in enumerate(annotated_tokens):
                            annotations = annotated_token.split('\t')
                            word, tag, ner = annotations[0], annotations[1], annotations[3]

                            # Get only the primary category
                            if ner != 'O':
                                ner = ner.split('-')[0]

                            # if tag in ('LQU', 'RQU'):
                            #     tag = "``"

                            standard_form_tokens.append((word, tag, ner))
                        conll_tokens = to_conll_iob(standard_form_tokens)

                        yield conlltags2tree(conll_tokens)
                        # yield [((w, t), iob) for w, t, iob in conll_tokens]

                        # ner_tags[ner] += 1


# print(ner_tags)
def to_conll_iob(annotated_sentence):

    proper_iob_tokens = []
    for idx, annotated_token in enumerate(annotated_sentence):
        tag, word, ner = annotated_token

        if ner != 'O':
            if idx == 0:
                ner = "B-" + ner
            elif annotated_sentence[idx - 1][2] == ner:
                ner = "I-" + ner
            else:
                ner = "B-" + ner
        proper_iob_tokens.append((tag, word, ner))

    return proper_iob_tokens


# Training your own system

"""
def features(tokens, index, history):

# tokens = a POS - tagged sentences
# index = the index of the token we want to extract features for
# history = the previous predicated IOB tags



    # init the SnowballStemmer
    stemmer = SnowballStemmer('english')

    # pad the sequences with the placeholders
    tokens = [('[START2]', '[START2]'), ('[START1]', '[START1]')] + \
        list(tokens) + [('[END1]', '[END1]'), ('[END2]', '[END2]')]
    history = ['[START2]', '[START1]'] + list(history)

    # shift the index with 2, to accommadate the padding
    index += 2

    word, pos = tokens[index]
    prevword, prevpos = tokens[index - 1]
    prevprevword, prevprevpos = tokens[index - 2]
    nextword, nextpos = tokens[index + 1]
    nextnextword, nextnextpos = tokens[index + 2]
    previob = history[index - 1]
    # prevpreviob = history[index - 2]

# contains_dash = '-' in word
# contains_dot = '.' in word
# allascii = all([True for c in word if c in string.ascii_lowercase])

# allcaps = word == word.capitalize()
# capitalized = word[0] in string.ascii_uppercase
#
# prevallcaps = prevword == prevword.capitalize()
# prevcapitalized = prevword[0] in string.ascii_uppercase
#
# nextallcaps = prevword == prevword.capitalize()
# nextcapitalized = prevword[0] in string.ascii_uppercase


    return {
        'word': word,
        'lemma': stemmer.stem(word),
        'pos': pos,
        'shap': shape(word),

        'nextword': nextword,
        'next-lemma': stemmer.stem(nextword),
        'next-pos': nextpos,
        'next-shape': shape(nextword),

        'next-next-word': nextnextword,
        'next-next-pos': nextnextpos,
        'next-next-lemma': stemmer.stem(nextnextword),
        'next-next-shape': shape(nextnextword),

        'prev-word': prevword,
        'prev-lemma': stemmer.stem(prevprevword),
        'prev-pos': prevpos,
        'prev-iob': previob,
        'prev-shape': shape(prevword),

        'prev-prev-word': prevprevword,
        'prev-prev-pos': prevprevpos,
        'prev-prev-lemma': stemmer.stem(prevprevword),
        'prev-prev-iob': prevpreviob,
        'prev-prev-shape': shape(prevprevword),


    # 'prev-iob': previob,
    #
    # 'contains-dash': contains_dash,
    # 'contains-dot': contains_dot,
    #
    # 'all-caps': allcaps,
    # 'capitalized': capitalized,
    #
    # 'prev-all-caps': prevallcaps,
    # 'prev-capitalized': prevcapitalized,
    #
    # 'next-all-caps': nextallcaps,
    # 'next-capitalized': nextcapitalized,


    }

"""
stemmer = SnowballStemmer('english')


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

# reader = read_gmb(corpus_root)
# l = list(reader)
# l[1]

# print(reader[0])
# for i in reader:
#    print(i)
