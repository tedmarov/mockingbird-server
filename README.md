<!-- /Using Rare; keep grinding away -->

# Mockingbird
mockingbird created by GH and VS

# Mockingbird

## **Description**
Mockingbird helps users memorize text.
 
## **Features**

## **Setup Server-Side**
 
### Pull down the Server-Side Repo.
 
>Note: This project is meant to run simultaneously with the Client Side Repo found here: https://github.com/nss-day-cohort-44/rare-client-fanciful-snowflake*  
>Depending on which repo you start with, you may already have the following directories set up. 
>This project requires Python
 
### To Begin installing the Server-Side Repo, complete the following steps: 
 
1. Create a directory from which to deploy the application. 	
```mkdir RARE```
 
2.   Enter the following commands: 

```git clone git@github.com:nss-day-cohort-44/rare-rest-api-fanciful-snowflake.git server .```        _note the single dot preceded by a single space_

```pip install django```
or if that doesn't work
```pip3 install django```
 
```pipenv install django autopep8 pylint djangorestframework django-cors-headers pylint-django``` 
 
3. Create a seed.sh file and run it

```
Create a seed.sh file in your project directory
Place the code below in the file.

#!/bin/bash

rm -rf rareapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations rareapi
python3 manage.py migrate rareapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata tags
python3 manage.py loaddata categories
python3 manage.py loaddata posts
python3 manage.py loaddata comments
python3 manage.py loaddata postTags
 
Run chmod +x seed.sh in the terminal.
Then run ./seed.sh in the terminal to run the commands.
```
 
## **Technologies Used**
This application was built using the React JavaScript library. The only package used in the production site outside of those provided by create-react-app was react-router-dom.
The API server is powered by SQLite, python3 and Python.
All styling was accomplished with vanilla CSS3 written by us.

## Planning Links
1. [ERD]()
1. Wireframe: 

# Author
[Ted Marov](https://github.com/tedmarov)

