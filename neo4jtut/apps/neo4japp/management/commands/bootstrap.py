# -*- coding: utf-8 -*-
__author__ = 'lundberg'


from django.core.management.base import BaseCommand
from apps.neo4japp.models import Movie, Person
from neo4jtut import db


class Command(BaseCommand):
    help = 'Create NodeHandle and set handle_id for nodes missing handle_id property'

    def handle(self, *args, **options):
        q = """
            MATCH (m:Movie) WHERE m.handle_id IS NULL WITH collect(id(m)) as movies
            MATCH (p:Person) WHERE p.handle_id IS NULL WITH movies, collect(id(p)) as persons
            RETURN movies, persons
            """
        with db.manager.read() as r:
            movies, persons = r.execute(q).fetchone()

        m, p = 0, 0
        for node_id in movies:
            movie = Movie.objects.create()
            with db.manager.write() as w:
                w.execute('START n=node({node_id}) SET n.handle_id = {handle_id}', node_id=node_id, handle_id=movie.pk)
            m += 1

        for node_id in persons:
            movie = Person.objects.create()
            with db.manager.write() as w:
                w.execute('START n=node({node_id}) SET n.handle_id = {handle_id}', node_id=node_id, handle_id=movie.pk)
            p += 1

        self.stdout.write('Successfully completed! Added %d movies and %d persons.' % (m, p))