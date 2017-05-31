import datetime

from django.http import HttpResponse
from django.shortcuts import render

from .forms import NameForm
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
            print(data['news_text'])
            data['news'] = rep(data['news'])
            data['news_text'] = rep(data['news_text'])
            print(data['news_text'])

            return render(request, 'news_ie/index.html', {'data': data, 'form': form})
            # return HttpResponse('/thanks')
    else:
        form = NameForm()

    return render(request, 'news_ie/index.html', {'form': form})
