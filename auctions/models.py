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
    image = models.ImageField(upload_to='images/', blank=False)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return {
            "id": self.id,
            "title": self.title,
            "seller":self.seller,
            "description":self.description,
            "image":self.image,
            "timestamp": self.timestamp.strftime("%A | %I:%M %p | %d %B, %Y"),
        }