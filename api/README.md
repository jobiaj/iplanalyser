
IplAnalyser quickstart: Django


This application can brought up using docker compose up.

If you have docker-compose is available in your local pull the code and move to base directory and run
sudo docker-compose up --build to bring up the application.

You can go to the browser after that application comes up.: http://localhost:8000/iplanalyser/year_summary/(%3FP2013%5Cd+)/


Please follow following steps the conventional way to bring the application Up:

This is a Django project that will fetch the data from the csv and display the highlights and graphs based on selected seasons.

NOTE: This version build with Python 3.8 and Django 3.2.6.

The steps in this document assume that you have access to an IplAnalyser Repo.

What has been done for you
This is a minimal Django 1.11 project. It was created with these steps:

Create a virtualenv
Manually install Django and other dependencies
pip freeze > requirements.txt
django-admin startproject project .
Update project/settings.py to configure SECRET_KEY, DATABASE and STATIC_ROOT entries
./manage.py startapp welcome, to create the welcome page's app
From this initial state you can:

create new Django apps
remove the welcome app
rename the Django project
update settings to suit your needs
install more Python libraries and add them to the requirements.txt file


requirements.txt   - list of dependencies

Database configuration
This application using the postgres database. 
Django & Postgres
First, we’ll add Postgres to our Django app. If you haven’t done that before, I suggest reading this wonderful tutorial from DigitalOcean.

Link : https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04

We need psycopg2, so we install it – pip install psycopg2 & add it to requirements.txt
Second, we need to update the database information in the settings.py. I have added a local_settings.py, You can add the DATABASE Changes in local_settings.py also.


Running the application in local:


git clone https://github.com/jobiaj/iplanalyser.git

Create database and update the db details in settings.py.

Create the virtual environment, and activate the environment.

pip install -r requirements.txt

move to the base folder where manage.py located and run python manage.py migrate

Then we need to load the data to the database from the csv. 
Run:
python manage.py load_match
python manage.py load_deliveries


If everything is alright, you should be able to start the Django development server:

python manage.py runserver 0.0.0.0:8000

Open your browser and go to http://127.0.0.1:8000/iplanalyser, you will be greeted with a welcome page.


You can see the demo of the application in:

https://iplanalyser.herokuapp.com/iplanalyser/
