from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

# Change the path according to your system
stanford_classifier='/home/amit/stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz'
stanford_ner_path = '/home/amit/stanford-ner-2016-10-31/stanford-ner.jar'
# Creating Tagger Object
st = StanfordNERTagger(stanford_classifier, stanford_ner_path, encoding='utf-8')
text = "Elderly woman killed in Jhapa pick-up van hit Damak Mar 11, 2017- An elderly woman died after being hit by a pick-up van at Lakhanpur in Jhapa district on Saturday."
# "The deceased has been identified as Man Maya Adhikari, 73, of Lakhanpur-1.
# Police Inspector Milan Basnet of the Area Police Office, Damak, informed that the vehicle (Me 1 Cha 3736) hit Adhikari while she was crossing the road.
# Critically injured in the incident, Adhikari breathed her last during the course of treatment at the Lifeline Hospital in Damak.
# text = ['While','in','France',",",'Christine','Lagarde','discussed']


def getlocation(text):
    location = []
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    for text in classified_text:
        if 'LOCATION' in text:
            location.append(text[0])
    return location


# print(classified_text)
