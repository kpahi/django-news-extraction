from django.shortcuts import render_to_response
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from news_ie.models import News

# Create your views here.


def index(request):
    # news = News.objects.all()
    news = News.objects.filter(date__range=["2017-06-20", "2017-06-24"])
    return render_to_response('news/index.html', {
        'news': news,
    })


class NewsListView(ListView):
    model = News
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['news'] = News.objects.all()

        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['news'] = News.objects.all()

        return context
