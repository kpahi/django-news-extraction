"""geodjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from news import views
from rss import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', views.index, name='index'),
    url(r'', include('rss.urls')),
    url(r'^news_ie/', include('news_ie.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^rssdb/', include('rssdb.urls')),
    url(r'^aboutUs/', include('aboutUs.urls')),





    #url(r'^', include('world.urls')),
]
