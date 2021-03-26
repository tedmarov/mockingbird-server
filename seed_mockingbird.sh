#!/bin/bash

rm -rf serverapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations serverapi
python3 manage.py migrate serverapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata categories
python3 manage.py loaddata birdies
python3 manage.py loaddata texts
python3 manage.py loaddata voices
python3 manage.py loaddata birdietexts
python3 manage.py loaddata comments

# Create a seed.sh file in your project directory
# Place the code below in the file.
# Run chmod +x seed_mockingbird.sh in the terminal.
# Then run ./seed_mockingbird.sh in the terminal to run the commands.