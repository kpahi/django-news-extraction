from django.http import HttpResponse
from django.shortcuts import render_to_response

from .models import WayPoint


# Create your views here.


def index(request):
    'Display Map'
    waypoints = WayPoint.objects.order_by('name')
    return render_to_response('world/index.html', {
        'waypoints': waypoints,
        #'content': render_to_response('world/waypoints.html', {'waypoints': 'waypoints'})
    })
