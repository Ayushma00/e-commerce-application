from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, AuctionListing, Watchlist, Bid,Comments
from django.views.decorators.csrf import csrf_exempt
from django import forms
from .form import Auctionform, Bidform, Commentform

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
def insert_bid(request):
    # if "bid" in request.POST:
    if request.method == "POST":
        bid_form = Bidform(request.POST)
        if bid_form.is_valid():
            bid_price = bid_form.cleaned_data["bid_price"]
            auction_id = request.POST.get("auction_id")
            if bid_price <= 0:   
                return render(request, "auctions/error_handling.html", {
                "code": 400,
                "message": "Bid price must be greater than 0"
            })              
            try:
                auction = AuctionListing.objects.get(pk = auction_id)   
                user = User.objects.get(id = request.user.id)
            except AuctionListing.DoesNotExist:
                return render(request, "auctions/error_handling.html", {
                    "code": 404,
                    "message": "Auction id doesn't exist"
                })
            if auction.seller == user:
                return render (request, "auctions/error_handling.html", {
                    "code": 404,
                    "message": "Seller cannot bid"
                })
            
            highest_bid = Bid.objects.filter(auction=auction).order_by('-bid_price').first()
           
            if  bid_price > auction.price:
                # Add new bid to db
                new_bid = Bid(auction=auction, user=user, bid_price=bid_price)
                new_bid.save()

                # Update current highest price
                auction.price = bid_price
                auction.save()

                return HttpResponseRedirect("listing/" + auction_id)
            else:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Youre bid is too small"
                })
        else:
            return render(request, "auctions/error_handling.html", {
                "code": 400,
                "message": "Form is invalid"
            })
    return render(request, "auctions/error_handling.html", {
        "code": 405,
        "message": "Method Not Allowed"
    })   
            

@login_required(login_url="login")
def add_comments(request):
    if request.method == "POST":
        comment_form = Commentform(request.POST)
        if comment_form.is_valid():
            comments = comment_form.cleaned_data["comments"]
            auction_id = request.POST.get("auction_id")
            try:
                auction = AuctionListing.objects.get(pk = auction_id)   
                user = User.objects.get(id = request.user.id)
            except AuctionListing.DoesNotExist:
                return render(request, "auctions/error_handling.html", {
                    "code": 404,
                    "message": "Auction id doesn't exist"
                })
            comment = Comments(auction=auction, user=user, comments=comments)
            comment.save()

                # Update current highest price
                # auction.price = bid_price
                # auction.save()

            return HttpResponseRedirect("listing/" + auction_id)
        else:
            return render(request, "auctions/error_handling.html", {
                "code": 400,
                "message": "Form is invalid"
            })
    return render(request, "auctions/error_handling.html", {
        "code": 405,
        "message": "Method Not Allowed"
    }) 
            

@login_required(login_url="login")
def watchlist(request):
    if request.method == "POST":
        item_id=request.POST.get("auction_id")
        if request.POST.get("on_watchlist") == "True":
            watchlist_item_delete = Watchlist.objects.get(
                seller = request.user.id,
                auction = AuctionListing.objects.get(pk =item_id),
            )
            watchlist_item_delete.delete()
        else:
            try:
                watchlist_item = Watchlist( 
                    seller = User.objects.get(pk = request.user.id),
                    auction = AuctionListing.objects.get(pk =item_id),
                    
                )
                watchlist_item.save()
            except IntegrityError:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Auction is already on your watchlist"
                })
        return HttpResponseRedirect("../listing/"+(item_id))
    watchlist_items = Watchlist.objects.filter(seller=request.user.id)

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
    bid_amount = Bid.objects.filter(auction=id).count()
    highest_bid = Bid.objects.filter(auction=id).order_by('-bid_price').first()
    
    comments = Comments.objects.filter(auction=id).order_by('-time')

    if current_item.close_bid:
        if highest_bid is not None:
            winner = highest_bid.user

            # Diffrent view for winner, seller and other users
            if request.user.id == current_item.seller.id:
                return render(request, "auctions/sold.html", {
                    "auction": current_item,
                    "winner": winner
                })
            elif request.user.id == winner.id:
                return render(request, "auctions/bought.html", {
                    "auction": current_item
                })
        else:
            if request.user.id == current_item.seller.id:
                return render(request, "auctions/no_offer.html", {
                    "auction": current_item
                })

        return HttpResponse("Error - auction no longer available")
    else:
        if request.user.is_authenticated:
            watchlist_item=Watchlist.objects.filter(auction = id,seller = User.objects.get(id = request.user.id)).first()
            
            if watchlist_item is not None:
                on_watchlist = True
                
            else:
                on_watchlist = False
                
        else:
            on_watchlist = False
            

        if highest_bid is not None:
                if highest_bid.user == request.user.id:
                    bid_message = "Your bid is the highest bid"
                else:
                    bid_message = "Highest bid made by " + highest_bid.user.username
        else:
            bid_message = "No highest bid so far"

        
        

        return render(request,"auctions/listing.html",{
            "item":current_item,
            "on_watchlist": on_watchlist,
            "bid_amount":bid_amount,
            "bid_message":bid_message,
            "bidform": Bidform(),
            "commentform" : Commentform(),
            "comments" : comments
        })


def close_bid(request, auction_id):
    try:
        auction = AuctionListing.objects.get(pk = auction_id)
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/error_handling.html", {
            "code": 404,
            "message": "Auction id doesn't exist"
        })

    if request.method == "POST":
        auction.close_bid = True
        auction.save()
    elif request.method =="GET":
        return render(request, "auctions/error_handling.html", {
            "code": 404,
            "message": "Method not allowed"
        })
    return HttpResponseRedirect("/listing/" + auction_id)


def category(request,category):

    category_display = dict(AuctionListing.CATEGORY).get(category)
    print(category_display)
    # Check if the category code is valid
    if category_display is None:
        # If the category code is not recognized, return a 404 error
        return Http404("Category not found")  # You can create a custom 404 page

    # Filter listings based on the selected category
    listings = AuctionListing.objects.filter(category=category,close_bid=False)


    context = {
        'listings': listings,
        'category_display': category_display
    }
    return render(request, 'auctions/category.html', context)
    


@csrf_exempt
def auction_list (request):
    if request.method!="POST":
        return JsonResponse({"error": "POST request required"},status=400)
    data = json.loads(request.body)

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
