""" Extract location from the given sentence list
    Uses standford NER package for the extraction.
    """
    
from ner import getlocation

#location extraction function
def get_location(sentlist):
    location = "None"
    for sentence in sentlist:
        if location =="None" or location == []:
            location=getlocation(sentence)
            # print(location)
        else:
            break
    return location
