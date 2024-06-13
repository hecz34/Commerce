from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment, Watchlist


class ListingAdmin(admin.ModelAdmin):
    list_display = ("active", "id", "title", "category", "seller", "price")


class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "bid_amount")


# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Watchlist)
