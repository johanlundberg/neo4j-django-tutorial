from django.contrib import admin
from apps.neo4japp.models import Movie, Person

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    pass


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Movie, MovieAdmin)
admin.site.register(Person, PersonAdmin)
