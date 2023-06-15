from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    def __str__(self):
        return self.username


class Auction_listings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_listings")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    image = models.URLField(default="https://www.google.com/url?sa=i&url=https%3A%2F%2Fconsumercomplaintscourt.com%2Fno-payment-received-for-work%2F&psig=AOvVaw2JAnZ7uT_5SreEuGO6sD6r&ust=1684926815711000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCOiOrdCni_8CFQAAAAAdAAAAABAE")
    category = models.CharField(max_length=20)
    date_listed = models.DateTimeField(default=timezone.now)
    watchlist = models.ManyToManyField(User, null=True, related_name="mywatchlist")

    def __str__(self):
        return self.title


class Bids(models.Model):
    listing = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="my_bid")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="highest_bidder")
    bid_date = models.DateTimeField(default=None, null=True)
    counter = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Bid on {self.listing} by {self.bidder}. {self.active}"


class Comments(models.Model):
    item = models.ForeignKey(Auction_listings, on_delete=models.CASCADE, related_name="my_comment_section")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_comment")
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author)