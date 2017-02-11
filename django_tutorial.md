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
        - There are several different "views" that do different things
            - A view is the view people get when they open your webpage, and you can sepcify several different views for them to see
            - Use the regular expressions in your other file to determine which view to use
- The file `wsgi.py` interacts with the Apache server
- `settings.py` contains several defaults you may or may not want to change, including what kind of relational database to work with (default should be SQLite3)
- `admins.py` allows you to specify which models should be allowed for modification through the administrative page

- `python manage.py createsuperuser` allows you to open a Django administrative page that lets you see who has permission to modify your site, the history of changes you have made to your site
    - you can also modify your data and SQL database using Django's framework

##### Writing your first view
- `python manage.py startapp polls`
- open the file polls/views.py and write your desired code in it

<pre><code>
from django.http import HttpResponse

# The HttpResponse is the object that returns information to the client

def index(request):
    return HttpResponse("Hello world")

def results(request):
    return HttpResponse("And here's the other potential view")
</code></pre>

- You can write other files within `polls` and enter python code in them

<pre><code>
# Using regex to figure out which view to use

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'([0-9]+)', views.results, name='results'),
    ]
</pre></code>

- Django checks your code for errors every time you save it; checks in the shell
- Use polls/models.py to write your models for working with data

##### Migrations
- A migration involves the manipulation of data, columns, rows, etc in SQL to account for changes in your database or in your desires
    - Django is capable of doing the hard work of figuring out what changes need to be instituted in the SQL database in order to run your code

##### Working with the shell
- 'python manage.py shell' opens a shell very much like iPython3, but with some Django functionality as well
- running commands that rely on Django and then saving with `.save()` will save the changes made to your Django database
- Can use object notation you've created in models.py to save information to SQL, meaning you don't need to use SQL syntax or SELECT statements
    - Can add new rows/columns, retrieve rows/columns, use indices to find particular row/column cells, search for rows with certain primary keys

##### Creating Templates
- Templates are created in a different directory, polls/templates/
- Within this directory, you create ANOTHER subdirectory called `polls`, so now the directory you are in is `polls/templates/polls`
- Our view functions will be injecting information into the template, filling it in

- Can create HTML code using commands that interact with your Python objects and views

<pre><code>
# Written in an HTML file

{% if latest_question_list %}

    <ul>
    {% for question in latest_question_list %}
        <li><a href="{% url 'results' question.id %}">{{question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls available</p>
{% endif %}
</pre></code>

##### HTML Forms
- an HTML form is a tag that allows you to send information back to the server