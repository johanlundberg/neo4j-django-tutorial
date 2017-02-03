from re import escape
from django.conf import settings
from neo4jtut.contextmanager import Neo4jDBSessionManager

__author__ = 'lundberg'

manager = Neo4jDBSessionManager(settings.NEO4J_RESOURCE_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)


def get_node(handle_id, label):
    q = 'MATCH (n:%s { handle_id: {handle_id} }) RETURN n' % label  # Ugly hack
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            return record['n']


def delete_node(handle_id, label):
    q = '''
        MATCH (n:%s { handle_id: {handle_id} })
        OPTIONAL MATCH (n)-[r]-()
        DELETE n, r
        ''' % label
    with manager.session as s:
        s.run(q, {'handle_id': handle_id})


def wildcard_search(search_string):
    search_string = '(?i).*%s.*' % escape(search_string)
    q = """
        OPTIONAL MATCH (m:Movie) WHERE m.title =~ {search_string} WITH collect(m) as movies
        OPTIONAL MATCH (p:Person) WHERE p.name =~ {search_string} WITH movies, collect(p) as persons
        RETURN movies, persons
        """
    with manager.session as s:
        result = s.run(q, {'search_string': search_string})
        return list(result)


def get_actors(handle_id):
    q = """
        MATCH (n:Movie {handle_id: {handle_id}})<-[r:ACTED_IN]-(person)
        RETURN person.handle_id, r.roles
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['person.handle_id'], 'roles': record['r.roles']}


def get_directors(handle_id):
    q = """
        MATCH (n:Movie {handle_id: {handle_id}})<-[r:DIRECTED]-(person)
        RETURN person.handle_id
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['person.handle_id']}


def get_producers(handle_id):
    q = """
        MATCH (n:Movie {handle_id: {handle_id}})<-[r:PRODUCED]-(person)
        RETURN person.handle_id
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['person.handle_id']}


def get_writers(handle_id):
    q = """
        MATCH (n:Movie {handle_id: {handle_id}})<-[r:WROTE]-(person)
        RETURN person.handle_id
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['person.handle_id']}


def get_movies(handle_id):
    q = """
        MATCH (n:Person {handle_id: {handle_id}})-[r]->(movie)
        RETURN movie.handle_id, COLLECT(r) as relationships
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['movie.handle_id'], 'relationships': record['relationships']}
