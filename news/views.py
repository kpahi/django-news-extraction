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

def objectlist(request):
    model = News
    context= News.objects.raw('SELECT COUNT(location) as loc,SUM(id) as id FROM news_ie_news GROUP BY location ORDER BY location ASC')
    # context = News.objects.all()s
    content = News.objects.all()
    vecdict={}
    testlist =  []
    for vec in content:
        # testlist.append(vec.vehicle_no)
        vecjson = vec.vehicle_no
        for ke in vecjson.keys():
            if ke not in vecdict:
                vecdict[ke]= 1
            else:
                vecdict[ke]+=1
    del vecdict["null"]
    # context = News.objects.all()
    template_name = 'news/index.html'

    return render_to_response(template_name, {'news': context,'vehicle':vecdict,'allnews':content})

def get_req(request):
    if request.method == 'POST':

        return render_to_response('news/bydate.html', {
            'name': "Kritish",
            # 'starter': date_start,

        })
    else:
        return redirect('/news/')


# class NewsListView(ListView):
#     model = News
#     template_name = 'news/index.html'
#     # form = NewsFilterForm
#
#     # def get_date(request):
#     #     if request.method == 'POST':
#
#     def get_context_data(self, **kwargs):
#         context = super(NewsListView, self).get_context_data(**kwargs)
#         context['news'] = News.objects.raw('SELECT COUNT(location) as loc,SUM(id) as id FROM news_ie_news GROUP BY location ORDER BY location ASC')
#         context['vehicle'] = News.objects.all()
#         return context



class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['news'] = News.objects.all()

        return context
