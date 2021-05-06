import json

from django.shortcuts import render

from .models import User, Item, Order, OrderItem
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone

# SHARED LISTS.
sections = ["fruit and vegetables", "dairy products", "meat and fish", "drinks", "bakery"]

# PROJECT VIEWS.


# Authentication Section
def index(request):

    # redirect the employees to focus on their work
    for group in request.user.groups.all():
        print(group)
        if str(group) == "operator":
            print(group)
            return HttpResponseRedirect(reverse("operator"))
        elif str(group) == "deliveryman":
            print(group)
            return HttpResponseRedirect(reverse("deliveryman"))
        elif str(group) == "dataentry":
            print(group)
            return HttpResponseRedirect(reverse("dataentry"))

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
            user_group = Group.objects.get(name='customer')
            user_group.user_set.add(user)
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


def show_orders(request):
    orders = Order.objects.filter(user_client=request.user).exclude(state="delivered")
    return render(request, "delivery/orders.html", {
        "orders": orders
    })


def show_all_orders(request):
    orders = Order.objects.all().order_by("-id")
    preparing = Order.objects.filter(state="preparing")
    submitted = Order.objects.filter(state="submitted")
    delivered = Order.objects.filter(state="delivered").order_by("-id")
    return render(request, "delivery/operator.html", {
        "orders": orders,
        "preparing": preparing,
        "submitted": submitted,
        "delivered": delivered
    })


def show_delivery_orders(request):
    user = request.user
    orders = Order.objects.filter(user_delivery=user).filter(state="submitted")
    return render(request, "delivery/deliveryman.html", {
        "orders": orders
    })


def assign_deliveryman(request):
    # Receiving the order data from the post request
    order_id = request.POST["orderId"]
    delivery_name = request.POST["deliveryman"]

    # update order
    deliveryman = User.objects.get(username=delivery_name)
    order = Order.objects.get(pk=order_id)
    order.user_delivery = deliveryman
    order.state = "submitted"
    order.submitted_at = timezone.now()
    order.save()

    return HttpResponseRedirect(reverse("operator"))


def finish_order(request):
    # Receiving the order data from the post request
    order_id = request.POST.get("orderId")

    # update order
    order = Order.objects.get(pk=order_id)
    order.state = "delivered"
    delivered_at = timezone.now()
    order.save()

    return HttpResponseRedirect(reverse("deliveryman"))

# EDIT AND RESET PROFILE SECTION
def edit_profile(request):
    # Get the user
    user = request.user
    if request.method == "POST":
        # Get registeration values
        username = request.POST["username"]
        address = request.POST["address"]
        phone = request.POST["phone"]

        user.username = username
        user.address = address
        user.phone = phone
        try:
            user.save()
        except IntegrityError:
            return render(request, "delivery/edit_profile.html", {
                "message": "Invalid entries."
            })

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "delivery/edit_profile.html", {
            "user": user
        })
        

def reset_pwd(request):
    user = request.user
    if request.method == "POST":
        # Get registeration values
        old_password = request.POST.get("oldPassword")
        new_password = request.POST["newPassword"]
        conf_password = request.POST["confirmation"]

        print(user.password)
        print(old_password, new_password, conf_password)

        if not check_password(old_password, user.password):
            return render(request, "delivery/reset_password.html", {
                "message": "Invalid old password."
            })

        if new_password != conf_password:
            return render(request, "delivery/reset_password.html", {
                "message": "Passwords must match."
            })

        user.password = make_password(new_password)
        user.save()
        return HttpResponseRedirect(reverse("index"))
        
    else:
        return render(request, "delivery/reset_password.html")

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

@csrf_exempt
def make_order(request):
    data = json.loads(request.body)

    order = Order(
        user_client = request.user,
        received_at = timezone.now(),
        state = "preparing"
    )
    order.save()

    for obj in data:
        item = Item.objects.get(name=obj["name"])
        orderItem = OrderItem(order=order, item=item, amount=obj["amount"])
        orderItem.save()

    print(data)
    return HttpResponse(status=201)
