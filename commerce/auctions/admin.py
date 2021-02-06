from django.contrib import admin
from .models import Comment, Bid, Listing

# Register your models here.

# Admin for the Lisitng Model
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'title', 'created', 'starting_bid', 'active', 'category']
    prepopulated_fields = {'slug': ('title',)}


# Admin for the Comment Model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'comment', 'listing', 'created']


# Admin for the Bid Model
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bid_user', 'bidding', 'bid_listing']
