from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, AuctionListing, Watchlist
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .form import Auctionform

@login_required(login_url='login')
def create_listing(request):
    return render(request, "auctions/auction_list.html", {
        'form': Auctionform()
    })
@login_required(login_url="login")
def insert_listing(request):
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
                price = price,
                image = image
            )
            # auction = AuctionListing(user = request.User, **form.cleaned_data)
            auction.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            render(request, "auctions/auction_list.html",{'form':form})
    return render(request, "auctions/auction_list.html",{'form':Auctionform()})

@login_required(login_url="login")
def watchlist(request):
    if request.method == "POST":
        print(request.POST)
        item_id=request.POST.get("auction_id")
        print(item_id)
        try:
            auction = AuctionListing.objects.get(pk =item_id)
            user = User.objects.get(pk = request.user.id)
        except AuctionListing.DoesNotExist:
            return render(request, "auctions/error_handling.html", {
                "code": 404,
                "message": "Auction id doesn't exist"
            })
        if request.POST.get("on_watchlist") == "True":
            watchlist_item_delete = Watchlist.objects.filter(
                seller = user,
                auction = auction,
            )
            watchlist_item_delete.delete()
        else:
            try:
                watchlist_item = Watchlist(
                    auction = auction,
                    seller = user
                    
                )
                watchlist_item.save()
            except IntegrityError:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Auction is already on your watchlist"
                })
        # return HttpResponseRedirect("/"+item_id)
    print(User.objects.get(id=request.user.id))
    watchlist_auctions_ids = User.objects.get(id=request.user.id).Watchlist.values_list("auction")
    watchlist_items = AuctionListing.objects.filter(id__in=watchlist_auctions_ids, closed=False)

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

def index(request):
    listings=AuctionListing.objects.all().order_by('published_date')
    return render(request, "auctions/index.html",{"listings":listings})

def listing(request,id ):
    try:
        current_item=AuctionListing.objects.get(pk =id)
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/error_handling.html", {
            "code": 404,
            "message": "Auction id doesn't exist"
        })
    print(current_item)
    if request.user.is_authenticated:
        watchlist_item=Watchlist.objects.filter(auction = id,seller = User.objects.get(id = request.user.id)).first()
        print(watchlist_item)
        if watchlist_item is not None:
            on_watchlist = True
            print("IN the watchlist")
        else:
            on_watchlist = False
            print("Not in the watch list")
    else:
        on_watchlist = False
        print("not authenticate")
    print("---",on_watchlist)
    return render(request,"auctions/listing.html",{
        "item":current_item,
        "on_watchlist": on_watchlist
    })




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
