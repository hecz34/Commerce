from django import forms
from .models import *


class NewListingForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=25,
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={"class": "form-control description"}),
    )
    price = forms.IntegerField(
        label="Starting Bid",
        widget=forms.NumberInput(attrs={"class": "form-control price"}),
    )
    image_url = forms.CharField(
        label="Image URL",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


# Using ModelForm
# class NewListingForm(forms.ModelForm):
#     class Meta:
#         model = Listing
#         fields = "__all__"
#         exclude = ["seller", "datetime", "active"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["title"].label = "Title"
#         self.fields["title"].widget.attrs.update(
#             {"class": "form-control"}
#         )
#         self.fields["description"].label = "Description"
#         self.fields["description"].widget.attrs.update(
#             {"class": "form-control"}
#         )
#         self.fields["price"].label = "Starting Bid"
#         self.fields["price"].widget.attrs.update(
#             {"class": "form-control"}
#         )
#         self.fields["image_url"].label = "Image URL"
#         self.fields["image_url"].widget.attrs.update(
#             {"class": "form-control"}
#         )
