from django.contrib import admin
from .models import User, AuctionListing, Watchlist,Bid,Comments
# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comments)