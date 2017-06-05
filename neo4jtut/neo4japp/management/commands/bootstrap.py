# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.management.base import BaseCommand
from django.db import DatabaseError
import uuid
from neo4japp.models import Movie, Person
from neo4jtut import db

__author__ = 'lundberg'


class Command(BaseCommand):
    help = 'Create a NodeHandle and set handle_id for nodes missing handle_id property'

    def handle(self, *args, **options):
        with db.manager.session as s:
            s.run('CREATE CONSTRAINT ON (p:Person) ASSERT p.handle_id IS UNIQUE')
            s.run('CREATE CONSTRAINT ON (m:Movie) ASSERT m.handle_id IS UNIQUE')

            try:
                q = """
                    OPTIONAL MATCH (m:Movie) WHERE NOT exists(m.handle_id) WITH collect(id(m)) as movies
                    OPTIONAL MATCH (p:Person) WHERE NOT exists(p.handle_id) WITH movies, collect(id(p)) as persons
                    RETURN movies, persons
                    """

                record = s.run(q).single()
                movies = record['movies']
                persons = record['persons']
            except IndexError:
                movies, persons = [], []

        q = 'START n=node($node_id) SET n.handle_id = $handle_id'
        m, p = 0, 0
        movie_objs = []
        person_objs = []
        with db.manager.transaction as t:
            try:
                for node_id in movies:
                    movie = Movie(handle_id=str(uuid.uuid4()))
                    movie_objs.append(movie)
                    t.run(q, {'node_id': node_id, 'handle_id': movie.handle_id})
                    m += 1
            except Exception as e:
                raise e
            else:
                try:
                    Movie.objects.bulk_create(movie_objs)
                except DatabaseError as e:
                    raise e

        with db.manager.transaction as t:
            try:
                for node_id in persons:
                    person = Person(handle_id=str(uuid.uuid4()))
                    person_objs.append(person)
                    t.run(q, {'node_id': node_id, 'handle_id': person.handle_id})
                    p += 1
            except Exception as e:
                raise e
            else:
                try:
                    Person.objects.bulk_create(person_objs)
                except DatabaseError as e:
                    raise e

        self.stdout.write('Successfully completed! Added %d movies and %d persons.' % (m, p))
