from practnlptools.tools import Annotator


def get_semantic_roles(sen):
    deathverb = ['die', 'kill', 'crush', 'pass']
    injuryverb = ['injure', 'hurt', 'wound', 'harm', 'trauma']
    verbs = []
    death = "None"

    annotator = Annotator()
    srlList = annotator.getAnnotations(sen)['srl']
    for dic in srlList:
        for text in dic:
            if "V" in text:
                #dic[text] = lemmatizer.lemmatize(dic[text], 'v')
                verbs.append(dic[text])
    for dic in srlList:
        for text in dic:
            if dic[text] in deathverb:
                if "A1" in dic:
                    death = dic["A1"]
                else:
                    death = dic['A0']
            elif dic[text] in injuryverb:
                if "A0" in dic:
                    injury = dic["A0"]
                else:
                    injury = dic["A1"]

    return srlList
