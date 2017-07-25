#import cPickle
import itertools
import pickle

from nltk import tree2conlltags
from nltk.chunk import ChunkParserI
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline

import dill

from .ner_with_python import *


class ScikitLearnChunker(ChunkParserI):

    @classmethod
    def to_dataset(cls, parsed_sentences, feature_detector):
        """
        Transform a list of tagged sentences into a scikit-learn compatible POS dataset
        :param parsed_sentences:
        :param feature_detector:
        :return:
        """
        X, y = [], []
        for parsed in parsed_sentences:
            iob_tagged = tree2conlltags(parsed)
            words, tags, iob_tags = list(zip(*iob_tagged))

            tagged = list(zip(words, tags))

            for index in range(len(iob_tagged)):
                X.append(feature_detector(tagged, index, history=iob_tags[:index]))
                y.append(iob_tags[index])

        return X, y

    @classmethod
    def get_minibatch(cls, parsed_sentences, feature_detector, batch_size=500):
        batch = list(itertools.islice(parsed_sentences, batch_size))
        X, y = cls.to_dataset(batch, feature_detector)
        return X, y

    @classmethod
    def train(cls, parsed_sentences, feature_detector, all_classes, **kwargs):
        X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', 500))
        vectorizer = DictVectorizer(sparse=False)
        vectorizer.fit(X)

        clf = Perceptron(verbose=10, n_jobs=-1, n_iter=kwargs.get('n_iter', 5))

        while len(X):
            X = vectorizer.transform(X)
            clf.partial_fit(X, y, all_classes)
            X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', 500))

        clf = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', clf)
        ])

        return cls(clf, feature_detector)

    def __init__(self, classifier, feature_detector):
        self._classifier = classifier
        self._feature_detector = feature_detector

    def parse(self, tokens):
        """
        Chunk a tagged sentence
        :param tokens: List of words [(w1, t1), (w2, t2), ...]
        :return: chunked sentence: nltk.Tree
        """
        history = []
        iob_tagged_tokens = []
        for index, (word, tag) in enumerate(tokens):
            iob_tag = self._classifier.predict([self._feature_detector(tokens, index, history)])[0]
            history.append(iob_tag)
            iob_tagged_tokens.append((word, tag, iob_tag))

        return conlltags2tree(iob_tagged_tokens)

    def score(self, parsed_sentences):
        """
        Compute the accuracy of the tagger for a list of test sentences
        :param parsed_sentences: List of parsed sentences: nltk.Tree
        :return: float 0.0 - 1.0
        """
        X_test, y_test = self.__class__.to_dataset(parsed_sentences, self._feature_detector)
        return self._classifier.score(X_test, y_test)


def train_perceptron():
    reader = read_gmb(corpus_root)

    all_classes = ['O', 'B-per', 'I-per', 'B-gpe', 'I-gpe',
                   'B-geo', 'I-geo', 'B-org', 'I-org', 'B-tim', 'I-tim',
                   'B-art', 'I-art', 'B-eve', 'I-eve', 'B-nat', 'I-nat']

    pa_ner = ScikitLearnChunker.train(itertools.islice(reader, 20), feature_detector=features,
                                      all_classes=all_classes, batch_size=2, n_iter=5)
    accuracy = pa_ner.score(itertools.islice(reader, 500))
    print("Accuracy:{}".format(accuracy))
    # save the model to disk
    filename = 'classifier_python3.pkl'
    pickle.dump(pa_ner, open(filename, 'wb'))

    loaded_model = dill.load(open(filename, 'rb'))
    output = loaded_model.parse(pos_tag(word_tokenize('I live in Nepal.')))
    print(output)

    # save the classifier
    # with open('my_dumped_classifier_3.pkl', 'w') as fid:
    #     pickle.dump(pa_ner, fid)
    #     fid.close()

    # joblibs
    # filename = 'classifier_python3.pkl'
    # with open(filename, 'wb') as fid:
    #     #joblib.dump(pa_ner, fid)

if __name__ == '__main__':
    train_perceptron()
