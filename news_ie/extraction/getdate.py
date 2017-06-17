""" Extract date from the sentence list
    Use regular expression to extract date only
    """

import datetime
import re

from .dates import DateService

service = DateService()

# date extraction function
def extract_date(sentlist):
    todaydate = datetime.datetime.now()
    exdate = "None"
    for sentence in sentlist:
        if exdate == "None" or exdate == todaydate:
            exdate = service.extractDate(sentence)
        else:
            break
    #extract date only from combination of date and time
    onlydate = re.findall(r'\d{4}.\d{2}.\d{2}',str(exdate))
    return onlydate
