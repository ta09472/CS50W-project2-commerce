from django import forms
from .models import Product,Bid

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','title', 'description', 'image_link','price']

class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bidding']
