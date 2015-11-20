# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import DatabaseError
import uuid
from apps.neo4japp.models import Movie, Person
from neo4jtut import db

__author__ = 'lundberg'

class Command(BaseCommand):
    help = 'Create a NodeHandle and set handle_id for nodes missing handle_id property'

    def handle(self, *args, **options):
        with db.manager.transaction as w:
            w.execute('CREATE INDEX ON :Person(handle_id)')
            w.execute('CREATE INDEX ON :Movie(handle_id)')
        q = """
            MATCH (m:Movie) WHERE m.handle_id IS NULL WITH collect(id(m)) as movies
            MATCH (p:Person) WHERE p.handle_id IS NULL WITH movies, collect(id(p)) as persons
            RETURN movies, persons
            """
        try:
            with db.manager.read as r:
                movies, persons = r.execute(q).fetchone()
        except IndexError:
            movies, persons = [], []

        q = 'START n=node({node_id}) SET n.handle_id = {handle_id}'
        m, p = 0, 0
        movie_objs = []
        person_objs = []
        with db.manager.transaction as w:
            try:
                for node_id in movies:
                    movie = Movie(handle_id=str(uuid.uuid4()))
                    movie_objs.append(movie)
                    w.execute(q, node_id=node_id, handle_id=movie.handle_id)
                    m += 1
            except Exception as e:
                raise e
            else:
                try:
                    Movie.objects.bulk_create(movie_objs)
                except DatabaseError as e:
                    w.connection.rollback()
                    raise e

        with db.manager.transaction as w:
            try:
                for node_id in persons:
                    person = Person(handle_id=str(uuid.uuid4()))
                    person_objs.append(person)
                    w.execute(q, node_id=node_id, handle_id=person.handle_id)
                    p += 1
            except Exception as e:
                raise e
            else:
                try:
                    Person.objects.bulk_create(person_objs)
                except DatabaseError as e:
                    w.connection.rollback()
                    raise e

        self.stdout.write('Successfully completed! Added %d movies and %d persons.' % (m, p))