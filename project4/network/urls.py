
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('following', views.following, name='following'),
    path('edit/', views.edit, name='edit'),
    path('<slug:username>/edit/', views.edit, name='edit'),
    path("<slug:username>/", views.user, name="user"),
    path('<slug:username>/follow/', views.follow, name='follow'),
    path('<slug:username>/like/<int:id>/', views.like, name='like'),
    path('like/<int:id>/', views.like, name='like'),
]
