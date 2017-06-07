""" Extract death and injury from the sentence list
    Compare with the death and injury verb to select the
    perfect predicate.
 """

from nltk.stem import WordNetLemmatizer
from practnlptools.tools import Annotator

from .sentoken import sentences
from .word_num import text2int

# instances
annotator = Annotator()
lemmatizer = WordNetLemmatizer()

# comparision verbs
deathverb = ['die', 'kill', 'crush', 'pass']
injuryverb = ['injure', 'sustain', 'critical', 'hurt', 'wound', 'harm', 'trauma']
verbs = []

# death extracting function


def death_no(sentlist):
    death = "None"
    for sent in sentlist:
        if death == "None":
            srlList = annotator.getAnnotations(sent)['srl']
            # print(srlList)
            for dic in srlList:
                for text in dic:
                    if "V" in text:
                        dic[text] = lemmatizer.lemmatize(dic[text], 'v')
                        verbs.append(dic[text])
            for dic in srlList:
                for text in dic:
                    if dic[text] in deathverb:
                        if "A1" in dic:
                            death = dic["A1"]
                        else:
                            death = dic['A0']

        else:
            break
    return death

# injury extraction function


def injury_no(sentlist):
    injury = "None"
    for sent in sentlist:
        if injury == "None":
            srlList = annotator.getAnnotations(sent)['srl']
            # print(srlList)
            for dic in srlList:
                for text in dic:
                    if text == "V":
                        dic[text] = lemmatizer.lemmatize(dic[text], 'v')
                        verbs.append(dic[text])
                        for dic in srlList:
                            for text in dic:
                                if dic[text] in injuryverb:
                                    if "A0" in dic:
                                        injury = dic["A0"]
                                    else:
                                        injury = dic["A1"]
        else:
            break
    return injury
