from django.shortcuts import render, render_to_response

from news_ie.extraction.vehicle_no import vehicle_no
from news_ie.models import News
from news_ie.views import extract_items, similar_story
from rssdb.models import rssdata

from django.views.generic.list import ListView

from .get_news import get_data_from_rss, rss, testaccidentnews
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.


def index(request):

    # from RSS feed get news list
    news_list = get_data_from_rss()
    newss = []
    # news_body
    for news in news_list:
        newss.append(str(news))
    # newss = [str(news[0]) for news in news_list]
    # print("lenght of news:")
    # print(len(newss))
    # headings
    headings = [post.title for post in rss.entries]
    indexes = []
    for headline in headings:
        if testaccidentnews(headline)== False:
            headings.remove(headline)
            indexes.append(headings.index(headline))
    newss = [v for i, v in enumerate(newss) if i not in indexes]
    # links
    links = [post.link for post in rss.entries]

    linkss = [v for i, v in enumerate(links) if i not in indexes]


    # combine the news headings and news body
    detailNews = dict(zip(headings, newss))

    # combine headings and links
    newsLinks = dict(zip(headings, linkss))

    # all news form db
    allNews = News.objects.all()

    allIndex = []
    newsStory = []

    for i, n in enumerate(newss):
        similarCoeff = []

        for dbNews in allNews:
            coeff = similar_story(n, dbNews.body)
            similarCoeff.append(coeff)

        if max(similarCoeff) > 0.60:
            print("Similary Story exists at index: ")
            newsIndex = similarCoeff.index(max(similarCoeff))
            print(newsIndex)
            story = allNews[newsIndex]
            newsStory.append(story)

            # allIndex.append(newsIndex)
            # newsStory = allNews[newsIndex]
            # print(newsStory.location)

        else:
            print("Extraction Requires")
            # print("Extracting:")
            story = extract_items(n)

            newsStory.append(story)
            # print("Extracting complete:")

            # story = News.objects.none()
            # newsStory.append(story)
            # newsStory[i] = "Extractions"
            # extract_items(n)

    # print(len(headings))
    # print(len(newsStory))
    # This line is main
    headingDetail = dict(zip(headings, newsStory))

    return render_to_response('rss/index.html', {
        'detailnews': detailNews,
        'newslinks': newsLinks,
        'newsstory': newsStory,
        'headingdetail': headingDetail,
    })

class RssListView(ListView):
    model = rssdata
    template_name = 'rss/index.html'
    paginate_by = 3

    # form = NewsFilterForm

    # def get_date(request):
    #     if request.method == 'POST':

    def get_context_data(self, **kwargs):
        context = super(RssListView, self).get_context_data(**kwargs)
        context['rssdb'] = rssdata.objects.all()

        return context
