# Neo4j and Django tutorial

This documentation will evolve as I spend time playing with the project.

# How to get started

Go to a directory of you choice and clone this repository:

```
git clone https://github.com/johanlundberg/neo4j-django-tutorial.git
cd neo4j-django-tutorial
```

Create virtualenv inside the repository and activate it:

```
virtualenv neo4j-django-tutorial
. neo4j-django-tutorial/bin/activate
```

Install the packages that you need:

```
pip install paver==1.2.2
pip install -r requirements.txt
```

Copy the generic Django setting file to settings.py and run syncdb:

```
cp neo4jtut/neo4jtut/generic_settings.py neo4jtut/neo4jtut/settings.py
python neo4jtut/manage.py syncdb
```

Download the latest Neo4j Community Edition from http://www.neo4j.org/download/.

Untar it anywhere and start it:

```
tar xvfz /path/to/neo4j-community-2.x.z-unix.tar.gz
cd neo4j-community-2.x.z-unix
bin/neo4j start
```

Go to http://localhost:7474 in your favorite browser and find a link called "The Movie Graph", click it. If not on
the front page it can be found when clicking the i-icon to the left. Click the arrow icon to the right in the
box that pops up and import the Cypher statement. Now you got some data in your graph.

Go back to your terminal window where you are in the repository directory and issue the following commands:

```
python neo4jtut/manage.py bootstrap
python neo4jtut/manage.py runserver
```

Go to http://localhost:8000 in your favorite browser to see the tutorial app.



