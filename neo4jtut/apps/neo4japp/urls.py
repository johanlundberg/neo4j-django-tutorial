# This also imports the include function
from django.conf.urls.defaults import *
from neo4jtut.apps.neo4japp.models import NodeHandle
from django.views.generic import ListView, DetailView

urlpatterns = patterns('neo4jtut.apps.neo4japp.views',
    # Index view
    (r'^$', 'index'),
    # localhost:8000/node/0/ should let Django know you wish to view node 0.
    (r'^node/(?P<node_id>\d+)/$', 'view_node'),
    # localhost:8000/relationship/0/ should let Django know you wish to view 
    # relationship 0.
    (r'^relationship/(?P<rel_id>\d+)/$', 'view_relationship'),
    # Django generic list view for NodeHandles
    (r'^nodehandles/$', ListView.as_view(model=NodeHandle, 
                                        context_object_name="handle_list"),),
    # Django generic detail view for NodeHandles
    (r'^nodehandle/(?P<pk>\d+)$', DetailView.as_view(model=NodeHandle,
        context_object_name="handle"), {}, "handle_detail"),
    # Cypher query view
    (r'^twitterfriends/$', 'twitterfriends'),
)