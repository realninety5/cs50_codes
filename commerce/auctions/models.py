from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass



class Listing(models.Model):
    ELECTRONICS = 'ET'
    FASHION = 'FS'
    HOME = 'HM'
    SPORT = 'SP'
    TOY = 'TY'
    AUTO = 'AU'

    PRODUCT_CATEGORY = [
        (ELECTRONICS, 'Electronics'),
        (FASHION, 'Fashion'),
        (HOME, 'Home'),
        (SPORT, 'Sport'),
        (TOY, 'Toy'),
        (AUTO, 'Auto'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='listing')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True, null=True)
    starting_bid = models.IntegerField()
    image = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=230, default='Null')
    category = models.CharField(max_length=2,
                                choices=PRODUCT_CATEGORY,
                                default=HOME, blank=True,
                                null=True,)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['created']


class Comment(models.Model):
    comment = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(User,
                                on_delete=models.CASCADE, related_name='commenter')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')
    title = models.CharField(max_length=250, default='Null')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.title}'


class Bid(models.Model):
    bid_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='bid_user')
    bidding = models.IntegerField()
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                related_name='bid_listing')


class WatchList(models.Model):
    w_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='w_user')
    w_listing = models.ForeignKey(Listing,
                             on_delete=models.CASCADE, related_name='w_listing')

