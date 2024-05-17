from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):

    FASHION ="FAS"
    ELECTRONICS ="ELE"
    FOOD = "FOO"
    DIY_HARDWARE ="DIY"
    MUSIC = "MUS"
    MOTORS = "MOT"
    BOOKS = "BOK"

    CATEGORY =[
        (FASHION,"Fashion"),
        (ELECTRONICS,"Electronics"),
        (FOOD,"Food"),
        (DIY_HARDWARE,"DIY & Hardware"),
        (MUSIC,"Music Instruments"),
        (MOTORS,"Motors"),
        (BOOKS,"Books")
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE,default="seller")
    title = models.CharField(max_length=100, blank = False)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=3, choices=CATEGORY, default=BOOKS)
    price = models.DecimalField(max_digits=11, decimal_places=2, default =0.0)
    image = models.URLField(max_length=200, blank=False)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}: by {self.seller}'

class Watchlist(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,default="auction")
    seller = models.ForeignKey(User, on_delete=models.CASCADE,default="watchlist")
    def __str__(self):
        return f'{self.auction.title}: by {self.seller} watchlist'
    

class Bid(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,default="auction")
    user = models.ForeignKey(User, on_delete=models.CASCADE,default="bidder")
    bid_price = models.DecimalField(max_digits=11, decimal_places=2, default =0.0)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} bid {self.auction.title} for {self.bid_price}'