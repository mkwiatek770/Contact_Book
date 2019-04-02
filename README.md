# Contact_Book
This project is a place where user can store his contacts.

## Technology Stack
* Python
* Django
* Bootstrap4

## Instalation
* clone repository from github using: git clone (adress)
* set up virtualenv (python 3 required!)
* activate virtualenv and install dependencies from requirements.txt:
* install psql if you don't have and change data in setting.py about your name, password etc. 
$ pip install -r requirements.txt
* go to directory where the manage.py is located and type:
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py runserver

## Usage
The Project allows users to store their contacts in one place - each contact has fields like:
* name
* surname 
* phone number(s)
* type of phone number (home, business purpose etc.)
* email adress(es)
* type of email (same as with phone)
* groups (friends, family, ...)

User can add new contacts and edit/delete existing ones.
User can add new groups and delete existring ones.

## Admin 
To get access to admin page in your console type:
* python manage.py createsuperuser
after creating admin user you will be able to have access to admin site on:
localhost:8000/admin 
There you can manually work with database tables.


