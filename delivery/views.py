from django.shortcuts import render

from .models import User, Item, Order
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# SHARED LISTS.
sections = ["Fruit and vegetables", "Dairy products", "Meat and fish", "Drinks", "Bakery"]

# PROJECT VIEWS.


# Authentication Section
def index(request):
    items = Item.objects.all().order_by('name')
    return render(request, "delivery/index.html", {
        "items": items
    })


def register(request):
    if request.method == "POST":

        # Get registeration values
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        address = request.POST["address"]
        phone = request.POST["phone"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "delivery/register.html", {
                "message": "Passwords must match."
            })

        # Create new user
        try:
            user = User.objects.create_user(username, email=None, password=password, address=address, phone=phone)
            user.save()
        except IntegrityError:
            return render(request, "delivery/register.html", {
                "message": "Username is already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "delivery/register.html")


def login_user(request):
    if request.method == "POST":

        # Login the user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "delivery/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "delivery/login.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Application Functions
def data_entry(request):
    if request.method == "POST":

        # Get item values
        name = request.POST["name"]
        description = request.POST["description"]
        category = request.POST.get("category")
        price = request.POST["price"]
        photoUrl = request.POST["photoUrl"]
        availability = request.POST.get("availability", "unavailable") == "available"

        # Validate the inputs
        if name == '' or description == '' or category == None or price == '' or photoUrl == '':
            return render(request, "delivery/dataentry.html", {
                "message": "Invalid Input value, fill all input fields and try again."
            })

        try:
            item = Item.objects.create(
                name=name,
                description=description,
                category=category,
                price=price,
                photo_url=photoUrl,
                availability=availability)
            item.save()
        except IntegrityError:
            return render(request, "delivery/dataentry.html", {
                "message": "This item is already registered."
            })

        return HttpResponseRedirect(reverse("dataentry"))

    else:
        items = Item.objects.all().order_by('-created_at')
        return render(request, "delivery/dataentry.html", {
            "items": items
        })