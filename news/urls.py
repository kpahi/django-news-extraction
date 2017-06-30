from django.conf.urls import url

from . import views
from .views import NewsDetailView, NewsListView

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', NewsListView.as_view(), name='news-list'),
    url(r'^(?P<slug>[-\w]+)/$', NewsDetailView.as_view(), name='news-detail'),

]
