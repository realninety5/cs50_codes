from django import forms
from .models import Listing, Comment, Bid


# Form to obtain Listing values from thr user
class ListingForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Title',
                                     'rows': '1', 'class': 'form-control'}), label='')
    description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Description',
                                     'rows': '5', 'class': 'form-control'}), label='')
    image = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Image URL',
                                     'rows': '1', 'class': 'form-control'}), label='')
    starting_bid = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Starting Bid',
                                     'rows': '1', 'class': 'form-control'}), label='')
    slug = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Slug',
                                     'rows': '1', 'class': 'form-control'}), label='')

    category = forms.Select(attrs={'class':'form-control'})

    class Meta:
        model = Listing
        fields = ['title', 'slug', 'description', 'category', 'starting_bid', 'image']



