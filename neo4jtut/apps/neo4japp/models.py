from django.db import models
from neo4jtut import db


# Create your models here.
class NodeHandle(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return 'NodeHandle for node %d' % self.node()[0]
        
    def node(self):
        return db.get_node(self.pk)


class Movie(NodeHandle):

    def __unicode__(self):
        return '%s' % self.node().get('title', 'Missing title')

    @models.permalink
    def get_absolute_url(self):
        return('neo4jtut.apps.neo4japp.views.movie_detail', (),
               {'handle_id': self.pk})


class Person(NodeHandle):

    def __unicode__(self):
        return '%s' % self.node().get('name', 'Missing name')

    @models.permalink
    def get_absolute_url(self):
        return('neo4jtut.apps.neo4japp.views.person_detail', (),
               {'handle_id': self.pk})