from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse as json

# Create your views here.

def home(request):
    return render(request, 'home.html',{})
