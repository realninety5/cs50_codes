from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('categories/', views.categories, name='categories'),
    path("register", views.register, name="register"),
    path('create/', views.create_listing, name='create_listing'),
    path('category/<item>/', views.category, name='category'),
    path('<username>/', views.user_page, name="user_page"),
    path('<username>/watchlist/', views.user_list,
         name='user_watchlist'),
    path('listing/<slug:item>/', views.list_item, name='list_item'),
    path('comment/<slug:item>/', views.comment, name='comment'),
    path('remove/<slug:slug>/', views.remove_bid, name='remove_bid'),
    path('listing/<slug:slug>/add_to_watchlist/', views.add_watchlist,
         name='add_watchlist'),
    path('listing/<slug:slug>/remove_watchlist/', views.remove_watchlist,
         name='remove_watchlist'),
]
