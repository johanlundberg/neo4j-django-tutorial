# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf.urls import url
from .views import MovieListView, MovieDetailView, PersonListView, PersonDetailView, index

__author__ = 'lundberg'

urlpatterns = [
    # Index view
    url(r'^$', index),
    url(r'^movies/$', MovieListView.as_view(), name='movie-list'),
    url(r'^movies/(?P<pk>[\d]+)/$', MovieDetailView.as_view(), name='movie-detail'),
    url(r'^persons/$', PersonListView.as_view(), name='person-list'),
    url(r'^persons/(?P<pk>[\d]+)/$', PersonDetailView.as_view(), name='person-detail'),
]