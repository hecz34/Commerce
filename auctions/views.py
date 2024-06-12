from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import Max
from .models import User, Category, Listing, Bid, Comment, Watchlist
from .forms import NewListingForm


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            Watchlist.objects.create(user=user)
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image_url = form.cleaned_data["image_url"]
            category_id = request.POST.get("category")
            category = Category.objects.get(pk=category_id)

            Listing.objects.create(
                title=title,
                description=description,
                price=price,
                image_url=image_url,
                category=category,
                seller=request.user,
            )
            return HttpResponseRedirect(reverse("index"))

    return render(
        request,
        "auctions/create.html",
        {"form": NewListingForm(), "is_editing": False},
    )


@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        form = NewListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(
        request,
        "auctions/create.html",
        {
            "form": NewListingForm(instance=listing),
            "is_editing": True,
            "listing_id": listing_id,
        },
    )


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    highest_bid = listing.listing_bids.order_by("-bid_amount").first()
    comments = listing.listing_comments.all()
    bid_msg = None
    in_watchlist = None
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(
            user=request.user, listings=listing
        ).exists()

    if request.method == "POST":
        user_bid = float(request.POST.get("bid"))
        if user_bid > listing.price:
            if highest_bid and user_bid <= highest_bid.bid_amount:
                bid_msg = "error"
            else:
                bid_msg = "success"
                if existing_bid := listing.listing_bids.filter(
                    user=request.user
                ).first():
                    existing_bid.delete()
                highest_bid = Bid.objects.create(
                    user=request.user, listing=listing, bid_amount=user_bid
                )
        else:
            bid_msg = "error"

    # Count total bids here incase new bid is submitted.
    total_bids = listing.listing_bids.count()
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "in_watchlist": in_watchlist,
            "total_bids": total_bids,
            "highest_bid": highest_bid,
            "bid_msg": bid_msg,
            "comments": comments,
        },
    )


@require_POST
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def watchlist(request, listing_id=None):
    watchlist = get_object_or_404(Watchlist, user=request.user)
    # watchlist = Watchlist.objects.get(user=request.user)
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        action = request.POST.get("action")
        if action == "add_to_watchlist":
            watchlist.listings.add(listing)
        else:
            watchlist.listings.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(
        request,
        "auctions/listings.html",
        {"title": "Watchlist", "listings": watchlist.listings.all()},
    )


@require_POST
def comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comment = request.POST.get("comment")
    Comment.objects.create(user=request.user, listing=listing, comment=comment)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def categories(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = category.category_listings.filter(active=True).all()
    return render(
        request,
        "auctions/listings.html",
        {"title": f"{category.name} Listings", "listings": listings},
    )
