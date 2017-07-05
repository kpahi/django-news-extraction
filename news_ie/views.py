import datetime
import string
import sys

from django.contrib.gis.geos import GEOSGeometry, Point, fromstr
from django.http import HttpResponse
from django.shortcuts import render

from world.models import WayPoint

from .extraction.getdate import extract_date
from .extraction.getdeathinjury import *
from .extraction.getnewlocation import geotraverseTree
from .extraction.ner import getlocation
from .extraction.vehicle_no import vehicle_no
from .extraction.getday import get_day
from .forms import NameForm
from .geocoder import *
from .models import News
from .sentoken import sentences
from .up import rep

# Create your views here.


def index(request):
    now = datetime.datetime.now()
    return render(request, 'news_ie/index.html', {'date': now})


def get_news(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        # To display waypoints on the maps
        waypoints = WayPoint.objects.order_by('name')

        if form.is_valid():
            story = News()
            data = form.cleaned_data
            story.body = data['news_text']

            #data['news'] = rep(data['news'])

            # print("Befor Splitting \n")
            # print(data['news_text'])
            #data['news_text'] = rep(data['news_text'])
            # Split the news into sentences [pre-processing]

            # Create Sentence Object
            sentclass = sentences()
            sentlist = sentclass.split_into_sentences(data['news_text'])
            splited_sen = []
            # print each sentences
            # print("\n" + "After Spliting " + "\n")
            for sent in sentlist:
                splited_sen.append(sent)
                # print(sent + "\n")

            sentences_dic = dict((i, splited_sen[i]) for i in range(0, len(splited_sen)))
            # print(sentences_dic)

            # Get the vehicle no. Here number_plate is the dictionary
            number_plate = vehicle_no(splited_sen)
            print(number_plate)
            story.vehicle_no = number_plate

            # Get death count and injury count

            death = death_no(splited_sen)
            print("Death No: ")
            print(death)
            story.death = death

            injury = injury_no(splited_sen)
            print("Injury No:")
            print(injury)
            story.injury = injury

            extdate = extract_date(sentlist)
            print("Date:", extdate)
            s = extdate[0]

            story.date = datetime.datetime.strptime(s, "%Y-%m-%d").date()

            # Get location from 1st sentences list
            # from the classifier
            location = geotraverseTree(splited_sen[0])
            print(location)
            story.location = location

            #Get day from the total sentence list
            day = get_day(sentlist)
            print(day)
            story.day = day

            # from standford, dont forget to use ' '.join(location)
            # location = getlocation(splited_sen[0])
            # print(' '.join(location))
            # story.location = ' '.join(location)

            # location_coordinates = find_lat_lng(location)

            try:
                location_coordinates = find_lat_lng(location)
            except Exception:
                location_coordinates = [0.0, 0.0]

            # print(location_coordinates[0])
            # print(location_coordinates[1])

            # Save the Coordinate of the location to Database as WayPoint
            lat = str(location_coordinates[0])
            lng = str(location_coordinates[1])
            #gem = "POINT(" + str(lat) + ' ' + str(lng) + ")"
            gem = GEOSGeometry('POINT(%s %s)' % (lng, lat))
            my_long_lat = lat + " " + lng
            gem = fromstr('POINT(' + my_long_lat + ')')
            WayPoint(name=' '.join(location), geometry=gem).save()

            # Now save the story
            # story.save()
            save_story(story, data)

            return render(request, 'news_ie/index.html', {'waypoints': waypoints, 'form': form, 'date': extdate,'day': day, 'sentences_dic': sentences_dic, 'death': death, 'injury': injury, 'number_plate': number_plate, 'location': location, 'coordintae': location_coordinates})
    else:
        form = NameForm()

    return render(request, 'news_ie/index.html', {'form': form})

# Save the story from the data
# Try Jaccard distance


def save_story(story, data):
    sim = []
    doc1 = set(data['news_text'].split())

    # get all the saved story
    savedStory = News.objects.all()
    for s in savedStory:
        doc2 = set(s.body.split())
        # find union
        union = list(doc1 | doc2)
        intersec = list(doc2.intersection(doc1))
        #intersection = list(set(doc1) - (set(doc1) - set(doc2)))
        jacc_coef = float(len(intersec)) / len(union)
        sim.append(jacc_coef)

    print(sim)
    jacc_max = max(sim)
    print(jacc_max)

    # set the threshold value to identify Duplicate

    thresHold = .90

    if jacc_max < thresHold:

        s = story.save()

        print("Save Successful:")
    else:
        print("Duplicate News Exists:")
