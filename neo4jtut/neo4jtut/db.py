from neo4j import contextmanager
from re import escape
from django.conf import settings
__author__ = 'lundberg'

manager = contextmanager.Neo4jDBConnectionManager(settings.NEO4J_RESOURCE_URI, settings.NEO4J_USERNAME,
                                                  settings.NEO4J_PASSWORD)


def get_node(handle_id, label):
    q = 'MATCH (n:%s { handle_id: {handle_id} }) RETURN n' % label  # Ugly hack
    try:
        with manager.read as r:
            for n in r.execute(q, handle_id=handle_id).fetchone():
                return n
    except IndexError:
        return {}


def delete_node(handle_id, label):
    q = '''
        MATCH (n:%s { handle_id: {handle_id} })
        OPTIONAL MATCH (n)-[r]-()
        DELETE n, r
        ''' % label
    with manager.transaction as w:
        w.execute(q, handle_id=handle_id)


def get_unique_node(label, key, value):
    q = 'MATCH (n:%s {%s: {value}}) RETURN n LIMIT 1' % (label, key)
    with manager.read as r:
        return r.execute(q, value=value).fetchone()


def wildcard_search(search_string):
    search_string = '(?i).*%s.*' % escape(search_string)
    q = """
        MATCH (m:Movie) WHERE m.title =~ {search_string} WITH collect(m) as movies
        MATCH (p:Person) WHERE p.name =~ {search_string} WITH movies, collect(p) as persons
        RETURN movies, persons
        """
    with manager.read as r:
        return r.execute(q, search_string=search_string).fetchone()


def get_actors(handle_id):
    q = """
        MATCH (n:Movie {handle_id: {handle_id}})<-[r:ACTED_IN]-(person)
        RETURN person.handle_id, r.roles
        """
    with manager.read as r:
        return r.execute(q, handle_id=handle_id).fetchall()


def get_directors(handle_id):
    q = """
        MATCH (n:Movie {handle_id: {handle_id}})<-[r:DIRECTED]-(person)
        RETURN person.handle_id
        """
    with manager.read as r:
        return r.execute(q, handle_id=handle_id).fetchall()


def get_producers(handle_id):
    q = """
        MATCH (n:Movie {handle_id: {handle_id}})<-[r:PRODUCED]-(person)
        RETURN person.handle_id
        """
    with manager.read as r:
        return r.execute(q, handle_id=handle_id).fetchall()


def get_writers(handle_id):
    q = """
        MATCH (n:Movie {handle_id: {handle_id}})<-[r:WROTE]-(person)
        RETURN person.handle_id
        """
    with manager.read as r:
        return r.execute(q, handle_id=handle_id).fetchall()

