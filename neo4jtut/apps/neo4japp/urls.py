# This also imports the include function
from django.conf.urls.defaults import *

urlpatterns = patterns('neo4jtut.apps.neo4japp.views',
    # Index view
    (r'^$', 'index'),
    # localhost:8000/node/0 should let Django know you wish to view node 0.
    (r'^node/(?P<node_id>\d+)/$', 'view_node'),
    # localhost:8000/relationship/0 should let Django know you wish to view 
    # relationship 0.
    (r'^relationship/(?P<rel_id>\d+)/$', 'view_relationship'),
)