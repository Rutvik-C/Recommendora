from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import json


def home_page(request):
    trending_movies = Movie.objects.all().order_by("-views")[:12]
    context_dictionary = {
        "trending_movies": trending_movies
    }

    if request.user.is_authenticated:
        # Do recommendations
        pass

    return render(request, "main/index.html", context_dictionary)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

        else:
            print("Invalid credentials")

    return redirect("app_home")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_again = request.POST.get("confirm_password")

        if not (User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists()):
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()

            user_preference = UserPreferences(
                user=new_user,
                feature_preference=json.dumps([0 for _ in range(36350)]),
                actor_preference=json.dumps([0 for _ in range(417200)]),
                director_preference=json.dumps([0 for _ in range(34705)]),
                studio_preference=json.dumps([0 for _ in range(31770)])
            )
            user_preference.save()

            login(request, new_user)
            print("User created")

        else:
            print("User already exists")

    return redirect("app_home")


def user_logout(request):
    logout(request)
    return redirect("app_home")

def search_movie(request):
    return render(request, 'main/searchmovie.html')

def user_profile(request):
    return render(request, 'main/userprofile.html')

def user_rate(request):
    return render(request, 'main/userrate.html')

def user_favorite(request):
    return render(request, 'main/userfavorite.html')