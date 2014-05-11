# Tests stolen from neo4jdb test_connection.py

import unittest
from db import Neo4jDBConnectionManager


class TestConnection(unittest.TestCase):

    def setUp(self):
        self.manager = Neo4jDBConnectionManager("http://localhost:7474")

    def tearDown(self):
        with self.manager.transaction() as cursor:
            cursor.execute("MATCH (n:TestCommit) DELETE n")

    def test_commit(self):
        # Given
        with self.manager.write() as cursor:
            cursor.execute("CREATE (n:TestCommit {name:1337})")

        # Other cursors should see it
        with self.manager.read() as cursor:
            cursor.execute("MATCH (n:TestCommit) RETURN n.name")
            self.assertEqual(cursor.fetchone(), (1337,))

        # And other connections should see it
        with self.manager.transaction() as cursor:
            cursor.execute("MATCH (n:TestCommit) RETURN n.name")
            self.assertEqual(cursor.fetchone(), (1337,))

    def test_read_and_commit(self):
        # Given
        with self.manager.write() as cursor:
            cursor.execute("CREATE (n:TestCommit {name:1337})")
            cursor.rowcount  # Force client to execute

        # Then other cursors should see it
        with self.manager.read() as cursor:
            cursor.execute("MATCH (n:TestCommit) RETURN n.name")
            self.assertEqual(cursor.fetchone(), (1337,))

        # And other connections should see it
        with self.manager.transaction() as cursor:
            cursor.execute("MATCH (n:TestCommit) RETURN n.name")
            self.assertEqual(cursor.fetchone(), (1337,))

    def test_rollback(self):
        # Given
        with self.manager.write() as cursor:
            cursor.execute("CREATE (n:TestRollback {name:1337})")
            # When
            cursor.connection.rollback()
            # Then the same cursor should not see it
            cursor.execute("MATCH (n:TestRollback) RETURN n.name")
            self.assertEqual(cursor.rowcount, 0)

        # And other connections should see it
        with self.manager.transaction() as cursor:
            cursor.execute("MATCH (n:TestRollback) RETURN n.name")
            self.assertEqual(cursor.rowcount, 0)


if __name__ == '__main__':
    unittest.main()