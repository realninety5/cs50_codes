from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search/', views.formview, name='search'),
    path('create/', views.create, name='create'),
    path('random/', views.random_page, name='random_page'),
    path('wiki/<TITLE>/', views.entry, name="entry"),
    path('wiki/edit/<title>/', views.editform, name='edit'),
]
