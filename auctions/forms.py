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
