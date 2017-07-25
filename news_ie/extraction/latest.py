
import os
import pickle
import sys

from nltk import conlltags2tree, pos_tag, tree2conlltags, word_tokenize
from nltk.chunk import ChunkParserI

from .my_data_defs import ScikitLearnChunker

# from .ner_with_python import features, read_gmb, shape, to_conll_iob

# from sklearn.feature_extraction import DictVectorizer
# from sklearn.linear_model import Perceptron
# from sklearn.pipeline import Pipeline


# import sk


DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(DIR, 'extraction')
filename = path + '/classifier_python3.pkl'
filename = '/home/kritish/geodjango/news_ie/extraction/classifier_python3.pkl'

s = "I live in Nepal."

# class ScikitLearnChunker(ChunkParserI):
#
#     @classmethod
#     def to_dataset(cls, parsed_sentences, feature_detector):
#         """
#         Transform a list of tagged sentences into a scikit-learn compatible POS dataset
#         :param parsed_sentences:
#         :param feature_detector:
#         :return:
#         """
#         X, y = [], []
#         for parsed in parsed_sentences:
#             iob_tagged = tree2conlltags(parsed)
#             words, tags, iob_tags = list(zip(*iob_tagged))
#
#             tagged = list(zip(words, tags))
#
#             for index in range(len(iob_tagged)):
#                 X.append(feature_detector(tagged, index, history=iob_tags[:index]))
#                 y.append(iob_tags[index])
#
#         return X, y
#
#     @classmethod
#     def get_minibatch(cls, parsed_sentences, feature_detector, batch_size=500):
#         batch = list(itertools.islice(parsed_sentences, batch_size))
#         X, y = cls.to_dataset(batch, feature_detector)
#         return X, y
#
#     @classmethod
#     def train(cls, parsed_sentences, feature_detector, all_classes, **kwargs):
#         X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', 500))
#         vectorizer = DictVectorizer(sparse=False)
#         vectorizer.fit(X)
#
#         clf = Perceptron(verbose=10, n_jobs=-1, n_iter=kwargs.get('n_iter', 5))
#
#         while len(X):
#             X = vectorizer.transform(X)
#             clf.partial_fit(X, y, all_classes)
#             X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', 500))
#
#         clf = Pipeline([
#             ('vectorizer', vectorizer),
#             ('classifier', clf)
#         ])
#
#         return cls(clf, feature_detector)
#
#     def __init__(self, classifier, feature_detector):
#         self._classifier = classifier
#         self._feature_detector = feature_detector
#
#     def parse(self, tokens):
#         """
#         Chunk a tagged sentence
#         :param tokens: List of words [(w1, t1), (w2, t2), ...]
#         :return: chunked sentence: nltk.Tree
#         """
#         history = []
#         iob_tagged_tokens = []
#         for index, (word, tag) in enumerate(tokens):
#             iob_tag = self._classifier.predict([self._feature_detector(tokens, index, history)])[0]
#             history.append(iob_tag)
#             iob_tagged_tokens.append((word, tag, iob_tag))
#
#         return conlltags2tree(iob_tagged_tokens)
#
#     def score(self, parsed_sentences):
#         """
#         Compute the accuracy of the tagger for a list of test sentences
#         :param parsed_sentences: List of parsed sentences: nltk.Tree
#         :return: float 0.0 - 1.0
#         """
#         X_test, y_test = self.__class__.to_dataset(parsed_sentences, self._feature_detector)
#         return self._classifier.score(X_test, y_test)


def main(s):
    # sent = sys.argv[1]
    # print(sys.argv[1])
    # filename = 'classifier_python3.pkl'
    loaded_model = pickle.load(open(filename, 'rb'))
    RESULT = loaded_model.parse(pos_tag(word_tokenize(s)))
    print(RESULT)

    return RESULT

if __name__ == '__main__':
    main("I live in Nepal")
