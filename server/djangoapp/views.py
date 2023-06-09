from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)





# Function for `about` view to render a static about page
def about(request):
     return render(request,'djangoapp/about.html')


# Functions for `contact` view to return a static contact page
def contact(request):
     return render(request,'djangoapp/contact.html')

# Functions for `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username,password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            messages.info(request, 'Your input is incorrect!')
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Functions for `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    messages.info(request, 'Logout success!')
    return render(request, 'djangoapp/index.html')


# Functions for `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Functions for `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Functions for `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

