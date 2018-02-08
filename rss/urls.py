from django.conf.urls import url

from . import views
from .views import RssListView

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', RssListView.as_view(), name='rss-list'),

]
