#!/bin/sh
#
# jbn@nordu.net - 2011
#

basedir="."
projname="$1"
appname="$2"

cd $basedir

if [ -d $projname/$appname ]; then
        echo "App $appname already exists"
        exit 1
fi

cd $basedir/$projname
echo " ** Creating app $appname in project $projname"
python manage.py startapp $appname
echo " ** Moving app to apps folder"
mv $appname apps
mkdir -p apps/$appname/templates/$appname
