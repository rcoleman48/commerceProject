from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Listing(models.Model):
    name = models.CharField(max_length=64)
    startingPrice = models.DecimalField(decimal_places=2, max_digits = 19)
    endDate = models.DateTimeField()
    picture = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=256)
    catChoices = [
        ('HM', 'Home'),
        ('FS', 'Fashion'),
        ('TY', 'Toys'),
        ('EL', 'electronics'),
        ('OT', 'Other'),
    ]
    category = models.CharField(
        max_length = 2,
        choices = catChoices,
        blank=True,
        null=True,
    )
    watcher = models.ManyToManyField(User, blank=True, related_name="watcher")
    poster = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=1, related_name="poster")
    
    
class Bids(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits = 19)
    user = models.ForeignKey(User, blank=True, default=1, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, blank=True, default=1, on_delete=models.CASCADE, related_name="productBid")
    
class Comments(models.Model):
    body = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=1, related_name="commenter")
    listing = models.ForeignKey(Listing, blank=True, on_delete=models.CASCADE, default=1, related_name="productComment")
    time = models.DateTimeField(auto_now=True)
