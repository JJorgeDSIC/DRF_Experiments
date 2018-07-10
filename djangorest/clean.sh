#!/bin/bash

echo "Cleaning everything up!"

rm -r db.sqlite3

rm -r api/migrations

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py makemigrations api

python3 manage.py migrate api


#python3 manage.py createsuperuser --username admin --email admin@example.com

python3 manage.py shell < userCreation.py

#execfile('pathToThePythonScriptPreviouslyCreated')
