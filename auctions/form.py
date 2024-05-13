from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from .models import User, AuctionListing

class Auctionform(ModelForm):
    # title = forms.CharField(label="Title",max_length=100, blank = False)
    # description = forms.TextField(label="Description",blank=True)
    # category = forms.CharField(label="Description",max_length=3, choices=CATEGORY, default=BOOKS)
    # price = forms.DecimalField(max_digits=11, decimal_places=2, default =0.0)
    # image = forms.ImageField(upload_to='images/', blank=False)
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "category", "price","image"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }