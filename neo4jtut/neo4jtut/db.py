__author__ = 'lundberg'

import neo4j
from contextlib import contextmanager


class Neo4jDBConnectionManager():

    """
    A helper class to manage connections with neo4jdb drivers to a Neo4j REST database.
    neo4jdb driver can be found here, https://github.com/jakewins/neo4jdb-python.

    Every new connection is a transaction. To minimize new connection overhead for many reads we try to reuse a single
    connection. If this seem like a bad idea some kind of connection pool might work better.

    Neo4jDBConnectionManager.read()
    When using with Neo4jDBConnectionManager.read(): we will always rollback the transaction. All exceptions will be
    thrown.

    Neo4jDBConnectionManager.write()
    When using with Neo4jDBConnectionManager.write() we will always commit the transaction except when we see an
    exception. If we get an exception we will rollback the transaction and throw the exception.

    Neo4jDBConnectionManager.transaction()
    When we don't want to share a connection (transaction context) we can set up a new connection which will work
    just as the write context manager above but with it's own connection.

    >>> manager = Neo4jDBConnectionManager("http://localhost:7474")
    >>> with manager.write() as w:
    ...     w.execute("CREATE (TheMatrix:Movie {title:'The Matrix', tagline:'Welcome to the Real World'})")
    ...
    <neo4j.cursor.Cursor object at 0xb6fafa4c>
    >>>
    >>> with manager.read() as r:
    ...     for n in r.execute("MATCH (n:Movie) RETURN n LIMIT 1"):
    ...         print n
    ({u'tagline': u'Welcome to the Real World', u'title': u'The Matrix'},)

    Commits in batches can be achieved by:
    >>> with manager.write() as w:
    ...     w.execute("CREATE (TheMatrix:Movie {title:'The Matrix Reloaded', tagline:'Free your mind.'})")
    ...     w.connection.commit()  # The Matric Reloaded will be committed
    ...     w.execute("CREATE (TheMatrix:Movie {title:'Matrix Revolutions', tagline:'Everything that has a beginning has an end.'})")
    """

    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = neo4j.connect(dsn)

    @contextmanager
    def read(self):
        try:
            yield self.connection.cursor()
        finally:
            self.connection.rollback()

    @contextmanager
    def write(self):
        try:
            yield self.connection.cursor()
        except neo4j.Connection.Error:
            self.connection.rollback()
        finally:
            self.connection.commit()

    @contextmanager
    def transaction(self):
        connection = neo4j.connect(self.dsn)
        try:
            yield connection.cursor()
        except neo4j.Connection.Error:
            connection.rollback()
        finally:
            connection.commit()
            connection.close()

