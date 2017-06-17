
from .models import *


"""
#Basic Algorithm
Get all the News objects
Each News objects body is a document
the news body from the form is new document
Compute the similarity between the News objects
document and form document
if similarity less then threshold, save to Database
else Duplicate News.

"""

# tokenize


# calcualte term frequency

# tf of term in the document


def tf(term, document):
    normalizeDocument = document.lower().split()
    return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))


def idf(term, allDocuments):
    numDocumentsWithThisTerm = 0
    for doc in allDocuments:
        if term.lower() in doc.lower().split():
            numDocumentsWithThisTerm += 1

    if numDocumentsWithThisTerm > 0:
        return 1.0 + log(float(len(allDocuments)) / numDocumentsWithThisTerm)
    else:
        return 1.0


qs = News.objects.all()
print(qs.count())
