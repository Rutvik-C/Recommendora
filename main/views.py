from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
import json
import pickle

with open("ml_utils/recommendation/feature_movie_rec.pkl", "rb") as f:
    model_feature = pickle.load(f)
with open("ml_utils/recommendation/actor_movie_rec.pkl", "rb") as f:
    model_actor = pickle.load(f)
with open("ml_utils/recommendation/director_movie_rec.pkl", "rb") as f:
    model_director = pickle.load(f)
with open("ml_utils/recommendation/studio_movie_rec.pkl", "rb") as f:
    model_studio = pickle.load(f)
with open("ml_utils/recommendation/feature_arrays.json", "r") as f:
    data = json.load(f)
with open("ml_utils/recommendation/feature_default.json", "r") as f:
    defaults = json.load(f)


def home_page(request):
    trending_movies = Movie.objects.all().order_by("-views")[:12]

    feature_rec, actor_rec, director_rec, studio_rec = [], [], [], []
    if request.user.is_authenticated:
        user_preference = UserPreferences.objects.get(user=request.user)

        feature_preference = json.loads(user_preference.feature_preference)
        actor_preference = json.loads(user_preference.actor_preference)
        director_preference = json.loads(user_preference.director_preference)
        studio_preference = json.loads(user_preference.studio_preference)

        y = data["title"]
        dist, ind = model_feature.kneighbors([feature_preference], n_neighbors=8)
        for i in ind[0]:
            feature_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_actor.kneighbors([actor_preference], n_neighbors=8)
        for i in ind[0]:
            actor_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_director.kneighbors([director_preference], n_neighbors=8)
        for i in ind[0]:
            director_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_studio.kneighbors([studio_preference], n_neighbors=8)
        for i in ind[0]:
            studio_rec.append(Movie.objects.filter(title=y[i]).first())

    context_dictionary = {
        "trending_movies": trending_movies,
        "feature_movies": feature_rec,
        "actor_movies": actor_rec,
        "director_movies": director_rec,
        "studio_movies": studio_rec
    }
    return render(request, "main/index.html", context_dictionary)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("app_home")

        else:
            messages.success(request, "Invalid credentials")
            return redirect("login")

    else:
        return render(request, "main/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_again = request.POST.get("confirm_password")

        if password != password_again:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username taken")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "E-Mail taken")
            return redirect("register")

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        user_preference = UserPreferences(
            user=new_user,
            feature_preference=defaults["feature"],
            actor_preference=defaults["actor"],
            director_preference=defaults["director"],
            studio_preference=defaults["studio"]
        )
        user_preference.save()

        login(request, new_user)
        return redirect("app_home")

    else:
        return render(request, "main/register.html")


def user_logout(request):
    logout(request)
    return redirect("app_home")


def search_movie(request):
    return render(request, 'main/searchmovie.html')


@login_required
def user_profile(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_new_password")

        user = authenticate(username=request.user.username, password=old_password)
        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully")

            else:
                messages.error(request, "Passwords do not match")

        else:
            messages.error(request, "Old password is incorrect")

        return redirect("user_profile")

    else:
        return render(request, 'main/userprofile.html')


def user_rate(request):
    return render(request, 'main/userrate.html')


def user_favorite(request):
    return render(request, 'main/userfavorite.html')
