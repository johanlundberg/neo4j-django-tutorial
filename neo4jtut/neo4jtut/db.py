__author__ = 'lundberg'

from neo4j import contextmanager
from re import escape

manager = contextmanager.Neo4jDBConnectionManager("http://localhost:7474")


def get_node(handle_id):
    q = 'START n=node:node_auto_index(handle_id={handle_id}) RETURN n LIMIT 1'
    try:
        with manager.read as r:
            for n in r.execute(q, handle_id=handle_id).fetchone():
                return n
    except IndexError:
        return {}


def delete_node(handle_id):
    q = '''
        START n=node:node_auto_index(handle_id={handle_id})
        OPTIONAL MATCH (n)-[r]-()
        DELETE n, r
        '''
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
