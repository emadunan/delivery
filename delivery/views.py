from django.shortcuts import render

from .models import User, Item, Order
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


# PROJECT VIEWS.

def index(request):
    if (request.user.is_authenticated):
        print(request.user.groups.all())
    
    return render(request, "delivery/index.html")


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
