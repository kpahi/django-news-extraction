from django.shortcuts import render_to_response
from django.views.generic.detail import DetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView

from news_ie.models import News

from .forms import NewsFilterForm

# Create your views here.


# def index(request):
#     # news = News.objects.all()
#     # form = NewsFilterForm()
#     news = News.objects.filter(date__range=["2017-06-20", "2017-06-24"])
#     return render_to_response('news/index.html', {
#         'news': news,
#         'name': "kritish"
#     })


def get_req(request):
    if request.method == 'POST':

        return render_to_response('news/bydate.html', {
            'name': "Kritish",
            # 'starter': date_start,

        })
    else:
        return redirect('/news/')


class NewsListView(ListView):
    model = News
    template_name = 'news/index.html'
    # form = NewsFilterForm

    # def get_date(request):
    #     if request.method == 'POST':

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['news'] = News.objects.all()
        # context['form'] = NewsFilterForm

        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['news'] = News.objects.all()

        return context
