from django import forms
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from .models import User, AuctionListing, Bid, Comments

class Auctionform(ModelForm):
    
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "category", "price", "image"]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your descriptions'}),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control mb-3'})

class Bidform(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_price"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

class Commentform(ModelForm):
    class Meta:
        model = Comments
        fields = ["comments"]
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
