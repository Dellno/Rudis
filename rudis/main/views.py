from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("<h2>вот тут писать html, файл находится по пути /Rudis/main/views.py <h2>")
