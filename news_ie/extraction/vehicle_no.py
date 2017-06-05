""" This script is for the extraction
of the Vehicle Number that are involved
the accident.
"""

import re
import sys


def prevword(target, source):
    target = '(' + target + ')'
    #print("Search this " + target)
    # print("In this " + source)
    #print("In this" + '\n')
    # This split the words conisidering the words inside braceket as one.
    source = re.findall('\[[^\]]*\]|\([^\)]*\)|\"[^\"]*\"|\S+', source)
    # print(source)
    for i, w in enumerate(source):
        if w == target:
            # return the word previous to the Number Plate
            return source[i - 1]


# This funciton returns the list of vehicled no. only. It
# needs to be identifed


def get_vehicle_no(sen):
    return re.findall(r'[A-Za-z ]+\d[0-9 ]+[A-Za-z ]+[0-9]+[0-9]', sen)


# get vehicle no as dictionary from the sentence list
def vehicle_no(sentlist):
    numberplate = []
    vehicle_type = []
    num_plate_dic = {}
    for sent in sentlist:
        # This split the words inside the bracket too. so not used.
        # print(sent.split('()'))
        if get_vehicle_no(sent):
            number = get_vehicle_no(sent)
            # Get the Vehicle Type
            for i in range(0, len(number)):
                if number[i] in sent:
                    vehicle_type.append(prevword(number[i], sent))
                numberplate.append(number[i])

            # if number[0] in sent:
            #     vehicle_type.append(prevword(number[0], sent))

    print(numberplate)
    print(vehicle_type)
    for i in range(0, len(numberplate)):
        if vehicle_type[i] in num_plate_dic.keys():
            num_plate_dic[vehicle_type[i]] += numberplate[i]
        else:
            num_plate_dic[vehicle_type[i]] = numberplate[i]

    # print(num_plate_dic)
    return num_plate_dic


# this function returns the dictionary of vehicle type and its vehicle no.
if __name__ == "__main__":
    d = vehicle_no(sentlist)
    print(d)
