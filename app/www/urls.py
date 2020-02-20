#-*- coding: utf-8 -*-
from django.conf.urls import include, url

from www.views.www.index import IndexView
from www.views.www.exhibitions import ExhibitionsView
from www.views.www.cv import CvView
from www.views.www.contact import ContactView
from www.views.www.gallery import GalleryListView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^nayttelyt/', ExhibitionsView.as_view(), name='exhibitions'),
    url(r'^galleria/', GalleryListView.as_view(), name='gallery'),
    url(r'^galleria/(?P<string>[\w\-]+)/$', GalleryListView.as_view(), name='gallery'), 
    url(r'^cv/', CvView.as_view(), name='cv'),
    url(r'^yhteys/', ContactView.as_view(), name='contact'),
]
