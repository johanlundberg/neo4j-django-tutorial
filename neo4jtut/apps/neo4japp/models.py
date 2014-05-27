from django.db import models
from django.core.urlresolvers import reverse
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
        return self.title

    def _title(self):
        return self.node().get('title', 'Missing title')
    title = property(_title)

    def get_absolute_url(self):
        return reverse('movie-detail', args=[str(self.id)])

    def _actors(self):
        actors = []
        for actor_id, roles in db.get_actors(self.handle_id):
            actors.append({'person': Person.objects.get(handle_id=actor_id), 'roles': roles})
        return actors
    actors = property(_actors)


class Person(NodeHandle):

    def __unicode__(self):
        return self.name

    def _name(self):
        return self.node().get('name', 'Missing name')
    name = property(_name)

    def get_absolute_url(self):
        return reverse('person-detail', args=[str(self.id)])