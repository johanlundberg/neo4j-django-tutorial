# Create your views here.
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from apps.neo4japp.models import Movie, Person
from neo4jtut import db


class MovieDetailView(DetailView):

    model = Movie


class MovieListView(ListView):

    model = Movie


class PersonDetailView(DetailView):

    model = Person


class PersonListView(ListView):

    model = Person


def index(request):
    return render(request, 'neo4japp/index.html')
