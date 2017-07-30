from django.conf.urls import url

from . import views
from .views import NewsDetailView

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.objectlist, name ='obj-list'),
    # url(r'^$', NewsListView.as_view(), name='news-list'),
    url(r'^(?P<slug>[-\w]+)/$', NewsDetailView.as_view(), name='news-detail'),
    url(r'^bydate', views.get_req, name='date'),

]
