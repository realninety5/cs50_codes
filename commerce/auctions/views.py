from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ListingForm
from .models import User, Listing, Comment, Bid, WatchList


def index(request):
    # Retrieve all listing and render them
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",
                  {'listings': listings})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    # If request is post, create a listing for this user
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            user.listing.create(user_id=user_id, title=form['title'], slug=form['slug'],
                                   description=form['description'], starting_bid=form['starting_bid'],
                                   image=form['image'], category=form['category'])
            return redirect('index')
        return render(request, 'auctions/create_listing.html',
                      {'form': form})
    # Else return a empty form
    return render(request, 'auctions/create_listing.html',
                  {'form': ListingForm()})


def list_item(request, item):
    # Retrieve thr necessary data
    comments = Comment.objects.filter(listing__slug=item)
    user = request.user.id
    item = Listing.objects.get(slug=item)
    if not user:
        return render(request, 'auctions/list_page.html', {'listing': item,
                           'comments': comments})

    user = User.objects.get(id=user)


    # If we already have a bid, get it;  else, max_bid = 0
    if Bid.objects.count() > 0:
        max_bid = max(Bid.objects.values_list('bidding', flat=True))
    else:
        max_bid = 0

    # If this user created the listing, give them the
    # privilege to close the auction
    if item.user_id_id == user.id:
        user_create = True
    else:
        user_create = False

    # If request is post, a bid has been made
    if request.method == "POST":
        bid = request.POST['bidding']

        # If bid is not digits or is empty, return the form
        if not bid.isdigit():
            return render(request, 'auctions/list_page.html',
                          {'listing': item, 'message': "Bid must be digits and not empty",
                           'bid_counts': Bid.objects.all().count(),
                           'users': user_create,
                           'comments': comments})
        bid = int(bid)

        # If the bid is lower than starting bid or
        # already existing bids, return the form
        if item.starting_bid > bid or max_bid >= bid:
            return render(request, 'auctions/list_page.html',
                              {'listing': item,
                               'message': "Bid must be up to Starting price and already bidded price",
                               'bid_counts': Bid.objects.all().count(),
                               'users': user_create,
                               'comments': comments})

        # Else create the form
        Bid.objects.create(bid_user=user, bidding=bid, bid_listing=item)
    return render(request, 'auctions/list_page.html', {'listing': item,
                                                 'bid_counts': Bid.objects.all().count(),
                                                       'users': user_create,
                                                       'comments': comments})
# Removes(make inactive) the auction from the listing
@login_required
def remove_bid(request, slug):
    item = get_object_or_404(Listing, slug=slug)
    # Check if there are bids already
    # if so, get the highest bid and declare its user the winner
    if item.bid_listing.all().count() > 0:
        winner = item.bid_listing.all().order_by('-bidding')[0]
        item.winner = winner.bid_user.username
        item.bid_listing.all().delete()
    item.active = False
    item.save()
    return redirect('list_item', slug)


# Adds a listing to the current user's
# watchlist
def add_watchlist(request, slug):
    user = request.user.id
    user = User.objects.get(id=user)
    item = slug
    slug = Listing.objects.get(slug=slug)
    w = user.w_user.create(w_user=user, w_listing=slug)
    w.save()
    return redirect('list_item', item)

# List all the listing posted by a particular user
def user_list(request, username):
    user = User.objects.get(username=username)
    user = user.w_user.all()
    return render(request, 'auctions/user_watchlist.html', {'listings': user})

# Removes a listing from this user's watchlist
def remove_watchlist(request, slug):
    user = request.user.id
    user = User.objects.get(id=user)
    slug = Listing.objects.get(slug=slug)
    item_to_delete = WatchList.objects.filter(w_user_id=user.id, w_listing_id=slug.id)[0]
    item_to_delete.delete()
    return redirect('user_watchlist', user.username)


# Returns the available categories
def categories(request):
    category_lists = Listing.PRODUCT_CATEGORY
    categories_list = dict(item for item in category_lists)
    return render(request, 'auctions/categories.html', {'categories': categories_list})


# Get the items in a particular category
def category(request, item):
    category_listings = Listing.objects.filter(category=item)
    # Get all the category items as a tuple and covert it to a dict
    category_lists = Listing.PRODUCT_CATEGORY
    categories_list = dict(item for item in category_lists)
    title = categories_list[item]
    return render(request, 'auctions/index.html', {'listings': category_listings, 'c_title': title})


# Return all listing by a particular user
def user_page(request, username):
    user_lists = Listing.objects.filter(user_id__username=username)
    return render(request, 'auctions/index.html', {'listings': user_lists,
                                            'u_title': username})
# Get the user and the posted comment
# and save them together
def comment(request, item):

    if request.method == "POST":
        title = request.POST['title']
        comment = request.POST['comment']
        user = request.user.id
        user = User.objects.get(id=user)
        listing = Listing.objects.get(slug=item)
        Comment.objects.create(user_id=user, title=title, comment=comment, listing=listing)

    return redirect('list_item', item)
