from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Questions")

def add_a_question(request):
    return HttpResponse("Add a question")

def current_question(request):
    return HttpResponse("Question name")