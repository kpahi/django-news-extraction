from django.http import HttpResponse
from django.shortcuts import render_to_response


# Create your views here.


def index(request):
    'Display Map'
    return render_to_response('world/index.html', {})
