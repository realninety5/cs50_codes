import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm

from .models import User, Posts, Following, Likes


def index(request):

    post = Posts.objects.all()
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            post = Posts.objects.create(body=form['body'], creator=user)
            post.save()
            postlike = Likes(post=post)
            postlike.save()
            post = Posts.objects.all()
            paginator = Paginator(post, 10)
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
            return render(request, 'network/index.html', {'posts': posts,
                                                          'form': PostForm(), 'like': postlike})
        return render(request, 'network/index.html', {'form': form})
    return render(request, 'network/index.html', {'form': PostForm(),
                                                  'posts': posts})


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user_f = Following(user=user)
            user_f.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def like(request, id, username=''):
    data = json.loads(request.body)
    id = data.get('post')
    try:
        post_liked = Posts.objects.get(id=id)
    except DoesNotExist:
        return HttpResponse(status=404)
    user = request.user.id
    user = User.objects.get(id=user)
    like, result = Likes.objects.get_or_create(post=post_liked)
    if user in like.liked_by.all():
        like.liked_by.remove(user)
    else:
        like.liked_by.add(user)
    like.save()
    return HttpResponse(status=204)


def user(request, username):
    if User.objects.filter(username=username):
        user = User.objects.get(username=username)
        posts = user.creator.all()
        page_number = request.GET.get('page')
        paginator = Paginator(posts, 10)
        posts = paginator.get_page(page_number)

        owner = request.user.username
        follows = Following.objects.get(user__username=owner)
        follows = follows in user.followed_by.all()

        return render(request, 'network/user.html',
                      {'posts': posts, 'follows': follows, 'w_user': user})
    else:
        return render(request, 'network/user.Html')


def following(request):

    user = request.user.id
    user = User.objects.get(id=user)
    result = User.objects.none()
    follows = user.followed_by.all()

    for item in follows:
        result = result | item.user.creator.all()

    result = result.order_by('-date')

    return render(request, 'network/following.html',
                  {'posts': result})

@csrf_exempt
def follow(request, username):
    user = request.user.username
    user_follow = User.objects.get(username=user)
    user = Following.objects.get(user__username=user)
    data = json.loads(request.body)
    username = User.objects.get(username=username)
    username.save()

    if request.method == 'PUT':
        if data.get('follow') == 'Unfollow':
            username.followed_by.remove(user)
            user_follow.num_people_followed -= 1
            user_follow.save()
        else:
            username.followed_by.add(user)
            user_follow.num_people_followed += 1
            user_follow.save()
        username.save()
    return HttpResponse(status=204)

@csrf_exempt
def edit(request):
    if request.method == "PUT":
        user = request.user.username
        user = User.objects.get(username=user)
        data = json.loads(request.body)
        old_body = data.get('old_body')
        new_body = data.get('new_body')

        post = Posts.objects.get(id=int(old_body))
        post.body = new_body
        post.save()
        return HttpResponse(status=204)
        pass
    else:
        return HttpResponse(status=404)
