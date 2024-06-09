from django import forms
from .models import *


class NewListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("name"),
        widget=forms.Select(attrs={"class": "custom-select"}),
    )

    class Meta:
        model = Listing
        fields = ["title", "description", "price", "image_url", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control description"}),
            "price": forms.NumberInput(attrs={"class": "form-control price"}),
            "image_url": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Title",
            "description": "Description",
            "price": "Price",
            "image_url": "Image URL",
            "category": "Category",
        }


# class NewListingForm(forms.Form):
#     title = forms.CharField(
#         label="Title",
#         max_length=25,
#         widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
#     )
#     description = forms.CharField(
#         label="Description",
#         widget=forms.Textarea(attrs={"class": "form-control description"}),
#     )
#     price = forms.IntegerField(
#         label="Starting Bid",
#         widget=forms.NumberInput(attrs={"class": "form-control price"}),
#     )
#     image_url = forms.CharField(
#         label="Image URL",
#         max_length=255,
#         required=False,
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#     )
