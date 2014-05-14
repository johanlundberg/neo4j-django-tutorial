from django.db import models
from neo4jtut import db


# Create your models here.
class NodeHandle(models.Model):
    handle_id = models.CharField(max_length=64, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return 'NodeHandle for node %d' % self.node()['handle_id']
        
    def node(self):
        return db.get_node(self.handle_id)

    def delete(self, **kwargs):
        """
                Delete that node handle and the handles node.
                """
        db.delete_node(self.handle_id)
        super(NodeHandle, self).delete()
        return True

    delete.alters_data = True


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