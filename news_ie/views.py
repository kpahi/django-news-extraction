import datetime
import string
import sys

from django.contrib.gis.geos import GEOSGeometry, Point, fromstr
from django.http import HttpResponse
from django.shortcuts import render

from world.models import WayPoint

from .extraction.ner import getlocation
from .extraction.vehicle_no import vehicle_no
from .forms import NameForm
from .geocoder import *
from .sentoken import sentences
from .up import rep


# Create your views here.


def index(request):
    now = datetime.datetime.now()
    return render(request, 'news_ie/index.html', {'date': now})


def get_news(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            #data['news'] = rep(data['news'])
            print("Befor Splitting \n")
            print(data['news_text'])
            #data['news_text'] = rep(data['news_text'])
            # Split the news into sentences [pre-processing]

            # Create Sentence Object
            sentclass = sentences()
            sentlist = sentclass.split_into_sentences(data['news_text'])
            splited_sen = []
            # print each sentences
            print("\n" + "After Spliting " + "\n")
            for sent in sentlist:
                splited_sen.append(sent)
                print(sent + "\n")

            sentences_dic = dict((i, splited_sen[i]) for i in range(0, len(splited_sen)))
            print(sentences_dic)

            # Get the vehicle no. Here number_plate is the dictionary
            number_plate = vehicle_no(splited_sen)
            print(number_plate)

            # Get location from 1st sentences list
            location = getlocation(splited_sen[0])
            print(location)

            location_coordinates = find_lat_lng(location)

            # print(location_coordinates[0])
            # print(location_coordinates[1])

            # Save the Coordinate of the location to Database as WayPoint
            lat = str(location_coordinates[0])
            lng = str(location_coordinates[1])
            #gem = "POINT(" + str(lat) + ' ' + str(lng) + ")"
            gem = GEOSGeometry('POINT(%s %s)' % (lng, lat))
            my_long_lat = lat + " " + lng
            #gem = fromstr('POINT(' + my_long_lat + ')')
            WayPoint(name=' '.join(location), geometry=gem).save()

            return render(request, 'news_ie/index.html', {'form': form, 'sentences_dic': sentences_dic, 'number_plate': number_plate, 'location': ' '.join(location), 'coordintae': location_coordinates})
    else:
        form = NameForm()

    return render(request, 'news_ie/index.html', {'form': form})
