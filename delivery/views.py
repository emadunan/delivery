import json

from django.shortcuts import render

from .models import User, Item, Order
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from django.views.decorators.csrf import csrf_exempt

# SHARED LISTS.
sections = ["Fruit and vegetables", "Dairy products", "Meat and fish", "Drinks", "Bakery"]

# PROJECT VIEWS.


# Authentication Section
def index(request):
    if request.method == "POST":

        filtered_items = Item.objects.filter(availability=True)
        if request.POST["category"]:
            category = request.POST["category"].lower()
            filtered_items = Item.objects.filter(category=category)
        if request.POST["name"]:
            name = request.POST["name"].lower()
            filtered_items = filtered_items.filter(name__contains=name)
        if request.POST["price_from"]:
            price_from = request.POST["price_from"]
            filtered_items = filtered_items.filter(price__gte=price_from)
        if request.POST["price_to"]:
            price_to = request.POST["price_to"]
            filtered_items = filtered_items.filter(price__lte=price_to)
        
        return render(request, "delivery/index.html", {
        "items": filtered_items.order_by('name')
        })
        
    else:
        items = Item.objects.filter(availability=True).order_by('name')
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
                name=name.lower(),
                description=description.lower(),
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


# API Functions

@csrf_exempt
def edit_item(request):

    data = json.loads(request.body)
    if data.get("id") is not None:
        try:
            item = Item.objects.get(pk=int(data["id"]))
        except Item.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

    # Receiving data from request body
    
    if data.get("name") is not None:
        item.name = data["name"]
    if data.get("description") is not None:
        item.description = data["description"]
    if data.get("category") is not None:
        item.category = data["category"]
    if data.get("price") is not None:
        item.price = data["price"]
    if data.get("photoUrl") is not None:
        item.photo_url = data["photoUrl"]
    if data.get("availability") is not None:
        item.availability = data["availability"] == "True"
        print(item.availability)
    
    item.save()
    return HttpResponse(status=204)