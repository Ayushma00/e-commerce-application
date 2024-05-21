# auctions/context_processors.py

from .models import AuctionListing

def categories(request):
    return {
        'categories': AuctionListing.CATEGORY
    }
