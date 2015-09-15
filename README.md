DD
==========

REQUIREMENTS
------------
    1.pgsql server
    2.python2.7
    3.python-pip
    4.psycopg2
    5.django 1.7
    6.pytz

1) Fork the repositery [DD](http://code.csiom.com/jasvir/project-management) and clone the forked repositery
    
    $ git clone 'link to your forked repository'

2) Create a database for DD.
3) Edit settings.py file. Things to be edited are:
    
    NAME : <db_name>
    USER : <db_user>
    PASSWORD : <db_password>

4) Goto the project directory and run the following commands.

    $ python manage.py syncdb
    $ python manage.py runserver
    
5) Open 'localhost:8000' in your browser.
