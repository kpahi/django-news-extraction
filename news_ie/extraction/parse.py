from .pre import ner

def parseday(sentences):
    day = "None"
    for sentence in sentences:
        if day == "None":
            ner_tags = ner(sentence)
            for tags in ner_tags:
                if "B-tim" in tags:
                    day = tags[0]
        else:
            break
    return day
def parselocation(sentence):
    location = []
    ner_tags = ner(sentence)
    for tags in ner_tags:
        if "B-geo" in tags or "I-geo" in tags:
            location.append(tags[0])
    strloc = (" ").join(location)
    return strloc

# sent = "A person died and four others were injured when a micro bus hit them at Jorpati, Kathmandu on Thursday."
#
# print(parselocation(sent))
# print(parseday(sent))
