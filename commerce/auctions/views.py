from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django import forms


#from .models import User
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows':5, 'cols':100}),
        }
        labels = {
            "body": "Write down your comment here",
        }

def index(request):
    listings = Auction_listings.objects.all()
    print(listings)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        global user
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
    

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["starting-bid"]
        image = request.POST["image-url"]
        category = request.POST["category"]

        if int(price)<1:
            return render(request, "auctions/create.html", {
                "message": "Price below 1 not allowed."
            })
        
        if request.user.is_authenticated:
            listing = Auction_listings(owner=request.user,title=title,description=description,price=price,image=image,category=category)
            listing.save()
            
            bid = Bids(listing=listing,bidder=request.user)
            bid.save()
        else:
            return render(request, "auctions/create.html", {
                "message": "Sign in required."
            })
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html")
    

def listings(request, pk, message=""):
    #listing_data = Auction_listings.objects.get(pk=pk)
    post = get_object_or_404(Auction_listings, pk=pk)
    comments = post.my_comment_section.all()
    comment_num = post.my_comment_section.all().count()
    listing = Auction_listings.objects.get(pk=pk)
    watchlisted = request.user in listing.watchlist.all()
    bid = Bids.objects.get(listing=listing)
    form = CommentForm()
    return render(request, "auctions/listing.html", {
        "pk": pk,
        "bid": bid,
        "listing": listing,
        "form": form,
        "count": comment_num,
        "comments": comments,
        "message": message,
        "watchlisted": watchlisted
    })



@login_required(login_url='login')
def bid(request,pk):
    amt = request.POST["bid-amount"]
    listin = Auction_listings.objects.get(pk=pk)

    if amt == "" or int(amt) <= listin.price+5:
        return listings(request,pk,"Invalid Bidding Amount")
        #return HttpResponseRedirect(reverse(listings, kwargs={"pk":pk}), {      # Why is this not working bro? 
        #    "message": "Did you really forgot to enter a bidding amount"})      # No errors on the screen yo

    listin.price = amt
    listin.save()
    bid = Bids.objects.get(listing=pk)
    print(bid)
    bid.bidder = request.user
    bid.counter+=1
    bid.save()

    return HttpResponseRedirect(reverse(listings, kwargs={"pk":pk}))


@login_required(login_url='login')
def comment(request, pk):
    post = get_object_or_404(Auction_listings, pk=pk)
    #qset = User.objects.first()
    #print(qset)
    #author = User.objects.get(pk=request.user.id)
    #print(author)        
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.item = post
        comment.author = request.user
        comment.save()
        return HttpResponseRedirect(reverse(listings,args=[pk]))
    
def close(request, pk):
    bid = Bids.objects.get(listing=pk)
    bid.active = False
    bid.save()
    return HttpResponseRedirect(reverse(listings, kwargs={"pk":pk}))


def watchlist(request):
    listings = request.user.mywatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def remove(request, pk):
    listing = Auction_listings.objects.get(pk=pk)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse(listings, kwargs={"pk":pk})) 

def add(request, pk):
    listing = Auction_listings.objects.get(pk=pk)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse(listings, kwargs={"pk":pk})) 

            

    