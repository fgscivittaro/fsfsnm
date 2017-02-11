from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"), # Acceses the home page if the string is empty
    url(r'add', views.add_a_question, name="add_question"), # Takes us to the add_a_question view
    url(r'(?P<question_id>[0-9]+)/current_question/$', 
    views.current_question, name="current_question"), # Acceses the current question

]
