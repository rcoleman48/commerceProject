from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.utils import timezone

from .models import User, Listing, Bids, Comments

catChoices = (
        ('HM', 'Home'),
        ('FS', 'Fashion'),
        ('TY', 'Toys'),
        ('EL', 'Electronics'),
        ('OT', 'Other'),
    )
    
def Active(end):
    if dt.datetime > end:
        return False
    return True

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    startingPrice = forms.DecimalField(decimal_places=2, max_digits = 19)
    endDate = forms.DateTimeField(widget=forms.DateTimeInput())
    picture = forms.URLField(required=False)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ChoiceField(
        widget = forms.RadioSelect(),
        choices = catChoices,
    )

def index(request):
    print(Listing.objects.all())
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "now": timezone.now()
    })


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
        
def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        title = request.POST["title"]
        startingPrice = request.POST["startingPrice"]
        endDate = request.POST["endDate"]
        picture = request.POST["picture"]
        description = request.POST["description"]
        category = request.POST["category"]
        l = Listing(name = title, startingPrice = startingPrice, endDate = endDate, picture = picture, description= description, category = category, poster=request.user)
        l.save()
        b = Bids(price = startingPrice, listing=l, user=request.user)
        b.save()
        return render(request, "auctions/listing.html", {
            "item": l,
            "bids": l.productBid.all(),
            "active": True,
            "max_bid": b,
            "comments": l.productComment.all(),
            "watching": Listing.objects.filter(id=l.id, watcher__username=request.user.username).exists()
        })
        
    return render(request, "auctions/create.html", {
        "form": NewListingForm()   
    })
    
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watcher.all()
    })
        
def listing(request, item_id):
    item = Listing.objects.get(id=item_id)
    bids = item.productBid.all()
    max_bid = bids.order_by('-id')[0]
    current_user = request.user
    if request.method == "POST":
        if request.POST.get("AddWatch"):
            request.user.watcher.add(item)
        if request.POST.get("RemoveWatch")=="Remove From Watchlist":
            item.watcher.remove(request.user)
            request.user.watcher.remove(item)
        if request.POST.get("Submit")=="Place Bid":
            print(item.startingPrice)
            if ((float(request.POST.get("Bid")) > item.startingPrice) and (float(request.POST.get("Bid")) > max_bid.price)):
                b = Bids(price=float(request.POST.get("Bid")), listing=item, user=current_user)
                b.save()
            else:
                return render(request, "auctions/listing.html", {
                    "item": item,
                    "bids": bids,
                    "error": True,
                    "active": item.endDate>timezone.now(),
                    "max_bid": max_bid,
                    "comments": item.productComment.all(),
                    "watching": Listing.objects.filter(id=item_id, watcher__username=current_user.username).exists()
                })
        if request.POST.get("Submit")=="Post Comment":
            c = Comments(body = request.POST.get("note"), user=current_user, listing=item)
            c.save()
        if request.POST.get("Submit")=="Close Auction":
            item.endDate = timezone.now()
            item.save()
    max_bid = bids.order_by('-id')[0]
    print(item.endDate>timezone.now())
    return render(request, "auctions/listing.html", {
        "item": item,
        "bids": bids,
        "active": item.endDate>timezone.now(),
        "max_bid": max_bid,
        "comments": item.productComment.all(),
        "watching": Listing.objects.filter(id=item_id, watcher__username=current_user.username).exists()
    })
    
def categories(request):
    return render(request, "auctions/categories.html")
    
def category(request, cat):
   for stuff in catChoices:
       if stuff[0] == cat:
           gory = stuff[1]
   print(Listing.objects.filter(category=cat))
   return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category=cat),
        "now": timezone.now(),
        "gory": gory
    })
