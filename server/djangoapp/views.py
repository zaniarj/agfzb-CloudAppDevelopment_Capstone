from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect,reverse
from .models import *
from .restapis import *
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
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect(reverse("djangoapp:index"))
        else:
            context={"msg":"Username already exists!"}
            return render(request, 'djangoapp/registration.html', context)  

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5f9594c6-e4a6-4467-91d6-9f87f14d2c0d/dealership-package/get-dealership/"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Functions for `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5f9594c6-e4a6-4467-91d6-9f87f14d2c0d/dealership-package/review"
        reviews = get_dealer_reviews_from_cf(url,str(dealer_id))
        context['review'] = reviews
    
    context['dealer_id'] = dealer_id
    print("get_dealer_details passed")
    print(context)
    return render(request, 'djangoapp/dealer_details.html', context)

# Functions for `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5f9594c6-e4a6-4467-91d6-9f87f14d2c0d/dealership-package/get-dealership/"
        dealer_name = get_dealers_from_cf(url)[dealer_id].full_name
        context = {
            "dealer_id": dealer_id,
            "dealer_name": dealer_name,
            "cars": CarModel.objects.all()
        }
        
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == "POST":
        url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/5f9594c6-e4a6-4467-91d6-9f87f14d2c0d/actions/dealership-package/post-review" 
        if request.user.is_authenticated:
            review = {}
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            print(request.POST["car"])
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
            json_result = post_request(url, review, dealerId=dealer_id)
           
            
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


