#!/bin/sh
#
# jbn@nordu.net - 2011
#

basedir="."
djangoadmin="env/bin/django-admin.py"
projname="$1"

cd $basedir

if [ -d $projname ]; then
        echo "Project $projname already exists"
        exit 1
fi

echo " ** Creating project $projname"
$djangoadmin startproject $projname
echo " ** Creating folderstructure"
cd $basedir/$projname
mkdir templates
mkdir static
mkdir static/img
mkdir static/css
mkdir static/js
mkdir static/upload
mkdir apps
echo " ** Creating basic files"
touch templates/base.html
touch static/css/style.css
touch apps/__init__.py
cd $basedir
if [ -x /usr/bin/tree ]; then
        tree $projname
        echo "--------------------------"
fi
echo " ** Project created!"

