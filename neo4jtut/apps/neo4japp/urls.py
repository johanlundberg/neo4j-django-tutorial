# -*- coding: utf-8 -*-
__author__ = 'lundberg'

from django.conf.urls import url, patterns
from apps.neo4japp.views import MovieListView, MovieDetailView

urlpatterns = patterns('apps.neo4japp.views',
    # Index view
    url(r'^$', 'index'),
    url(r'^movies/$', MovieListView.as_view(), name='movie-list'),
    url(r'^movies/(?P<pk>[\d]+)/$', MovieDetailView.as_view(), name='movie-detail'),
)