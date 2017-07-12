""" Extract death and injury from the sentence list
    Compare with the death and injury verb to select the
    perfect predicate.
 """

from nltk.stem import WordNetLemmatizer
from practnlptools.tools import Annotator

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
                                        # This indentation was backward
                                    else:
                                        injury = dic["A1"]
        else:
            break
    return injury


def convertNum(toconvert):

    toconvert = toconvert.lower()
    intconvert = text2int(toconvert)
    if intconvert.split() == toconvert.split():
        death_no = 1
        # print(death_no)
    else:
        checklist = intconvert.split(" ")
        # print(checklist)
        deathdigit = [int(s) for s in intconvert.split() if s.isdigit()]
        # print(deathdigit)
        for i in deathdigit:

            if i > 1900:
                point = checklist.index(str(i))
                checklist = checklist[point + 1:]
                dpoint = deathdigit.index(i)
                deathdigit = deathdigit[dpoint + 1:]
                # print(checklist)
                break
        if deathdigit == []:
            death_no = 1
        else:
            death_no = deathdigit[0]
    return death_no


def remove_date(toremove):
    toremove = toremove.replace('- ', ' ')
    checklist = toremove.split(" ")
    # print(checklist)
    deathdigit = [int(s) for s in toremove.split() if s.isdigit()]
    if deathdigit == []:
        value = checklist
    else:
        # print(deathdigit)
        for i in deathdigit:
            if i > 1900:
                point = checklist.index(str(i))
                checklist = checklist[point + 1:]
                deathdigit = deathdigit[point + 1:]
                # print(checklist)
                break
        value = checklist
    value = (" ").join(value)
    return value
