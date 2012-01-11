from django.db import models
import neo4jclient as nc

# Create your models here.
class NodeHandle(models.Model):
    node_id = models.BigIntegerField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'NodeHandle %d' % (self.node_id)
        
    def node(self):
        return nc.neo4jdb.nodes.get(self.node_id)
    
    @models.permalink
    def get_node_url(self):
        return('neo4jtut.apps.neo4japp.views.view_node', (),
               {'node_id': self.node_id})

    @models.permalink
    def get_absolute_url(self):
        return('handle_detail', (), {'pk': self.pk})
                