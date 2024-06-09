from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.get_full_name()


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    image_url = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category_listings",
        blank=True,
        null=True,
    )
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_listings"
    )
    datetime = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ID: {self.id}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_bids"
    )
    bid_amount = models.FloatField()

    def __str__(self):
        return (
            f"${self.bid_amount:.2f} {self.user.get_full_name()} {self.listing.title}"
        )


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_comments"
    )
    comment = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}  {self.listing.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_watchlist"
    )
    listings = models.ManyToManyField(Listing, related_name="listing_watchlist")

    def __str__(self):
        return f"{self.user.get_full_name()}"
