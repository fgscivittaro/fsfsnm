## Django

##### The Web
- Ex. The Washington Post (their website was created using Django)
    - The links to articles on their site are from a database
    - The article webpages are cached and then retrieved from the cache

- Files can be stored in three places:
    - The website's own server
    - Your browser
    - An intermediary

- Can use "View"-->"Developer"-->"Developer Tools" (works on Mac, not sure how to do it on PC)
- When we load a webpage, it takes in three kinds of files: HTML, CSS, and JavaScript
    - CSS is used for the style
        - Because it is very rarely changed, the CSS file is cached on your browser itself, which the website reuses every time you load a page

- Browsers can only run JavaScript
    - Interactions like the kind you perform on Google Maps are run through JavaScript code

##### Django's role
- The Process
    - The client sends an HTTP request to the server
    - The server, which has a set template, uses Django to retrieve data from a database
        - The desired data is inserted into the template
    - Django creates the HTML code on the fly and sends it back to the client

- All the information Django uses is stored in a database (SQL)
    - Treats each row in the database as an object of some class, which means we can interact with the database using Python object syntax

##### Django Tutorial
- To create a project, write `django-admin startproject mysite` in the shell
    - Creates a `mysite` outer directory
    - This directory contains the subdirectory `mysite/` and a file called `manage.py`
    - `python manage.py runserver` starts the actual Django server and assigns you a domain using your IP address

- The mysite inner directoy contains a file called `urls.py`
    - Tells Django which view to use
        - There are several different views that do different things
- The file `wsgi.py` interacts with the Apache server
- `settings.py` contains several defaults you may or may not want to change, including what kind of relational database to work with (default should be SQLite3)

##### Writing your first view
- `python manage.py startapp polls`
- open the file polls/views.py and write your desired code in it

"""
from django.http import HttpResponse

# The HttpResponse is the object that returns information to the client

def index(request):
    return HttpResponse("Hello world")
"""

- You can write other files within `polls` and enter python code in them

"""
from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.index, name='index'),]
# If the URL is an empty string, then return this view
"""

- Django checks your code for errors every time you save it; checks in the shell

##### Migrations
- A migration involves the manipulation of data, columns, rows, etc in SQL to account for changes in your database or in your desires