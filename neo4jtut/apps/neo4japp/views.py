# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from neo4jtut.apps.neo4japp.models import NodeHandle
import neo4jclient as nc

def index(request):
    return render_to_response('neo4japp/index.html', {},
                              context_instance=RequestContext(request))
                              
def view_node(request, node_id):
    node_id = int(node_id)
    node = nc.neo4jdb.nodes.get(node_id)
    node_handle, created = NodeHandle.objects.get_or_create(node_id=node_id)
    if created:
        node_handle.save()
    return render_to_response('neo4japp/node.html',
                              {'node': node, 'handle': node_handle},
                              context_instance=RequestContext(request))
                              
def view_relationship(request, rel_id):
    rel = nc.neo4jdb.relationships.get(int(rel_id))
    return render_to_response('neo4japp/relationship.html', 
                              {'relationship': rel},
                              context_instance=RequestContext(request))

def twitterfriends(request):
    '''
    This view assumes that you are using the Twitter sample Neo4j database
    from http://example-data.neo4j.org/files/.
    '''
    cypher_query = '''
        START users = node(2) 
        MATCH users-[:USER]->(user)-[:KNOWS]->(friend) 
        RETURN user, collect(friend) as collectfriends
        '''
    query = nc.neo4jdb.query(cypher_query)
    # If you run neo4j-embedded < 1.6.b3  you have to remove 
    # "as collectfriends" from the above query and uncomment line 40-43.
    #user_list = []
    #for hit in query:
    #    user_list.append({'user': hit['user'], 
    #                      'collectfriends': hit['collect(friend)']})
    return render_to_response('neo4japp/twitter_friends.html', 
                              {'user_list': query},
                              context_instance=RequestContext(request))
