from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, AuctionListing
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .form import Auctionform


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = Auctionform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            
            auction = AuctionListing(
                seller = User.objects.get(pk = request.user.id),
                title = title,
                description = description,
                category = category,
                image = image
            )
            auction.save()
        else:
            render(request, "auctions/auction_list.html",{'form':form})
    return render(request, "auctions/auction_list.html",{'form':Auctionform()})


def index(request):
    return render(request, "auctions/index.html")
@csrf_exempt
def auction_list (request):
    if request.method!="POST":
        return JsonResponse({"error": "POST request required"},status=400)
    data = json.loads(request.body)
    print(data)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
