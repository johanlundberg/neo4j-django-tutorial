# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 12:16:20 2012

@author: lundberg@nordu.net
"""
from neo4j import GraphDatabase

# Load Django settings
from django.conf import settings as django_settings
NEO4J_URI = django_settings.NEO4J_RESOURCE_URI

def open_db(uri=NEO4J_URI):
    '''
    Open or create a Neo4j database in the supplied path. As the module
    opens the database located at NEO4J_URI when imported you shouldn't have
    to use this.
    '''
    if uri:
        return GraphDatabase(uri, allow_store_upgrade='true')
    raise Exception('No NEO4J_URI set.')
        
# Open the database that is set in the Django settings NEO4J_RESOURCE_URI as 
# soon as the module is loaded.
try:
    neo4jdb = open_db()
except Exception as e:
    print '*** WARNING ***'
    print 'Error: %s' % e
    print 'Could not load the Neo4j database. Is it already loaded?'
    print 'Use open_db(URI) to open another database.'

def _close_db():
    try:
        neo4jdb.shutdown()
    except NameError:
        print 'Could not shutdown Neo4j database. Is it open in another process?'

import atexit
atexit.register(_close_db)