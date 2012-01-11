# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

import neo4jclient as nc

def index(request):
    return render_to_response('neo4japp/index.html', {},
                              context_instance=RequestContext(request))
                              
def view_node(request, node_id):
    node = nc.neo4jdb.nodes.get(int(node_id))
    return render_to_response('neo4japp/node.html', {'node': node},
                              context_instance=RequestContext(request))
                              
def view_relationship(request, rel_id):
    rel = nc.neo4jdb.relationships.get(int(rel_id))
    return render_to_response('neo4japp/relationship.html', 
                              {'relationship': rel},
                              context_instance=RequestContext(request))
