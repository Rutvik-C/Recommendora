from django.shortcuts import render, redirect
from django.contrib.auth.models import User
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


def home_page(request):
    print("Here")
    trending_movies = Movie.objects.all().order_by("-views")[:12]

    feature_rec, actor_rec, director_rec, studio_rec = [], [], [], []
    if request.user.is_authenticated:
        user_preference = UserPreferences.objects.get(user=request.user)

        feature_preference = json.loads(user_preference.feature_preference)
        actor_preference = json.loads(user_preference.actor_preference)
        director_preference = json.loads(user_preference.director_preference)
        studio_preference = json.loads(user_preference.studio_preference)
        print("Data Ready")

        y = data["title"]
        print("Starting rec")
        dist, ind = model_feature.kneighbors([feature_preference], n_neighbors=8)
        print("rec done 1")
        temp = [888, 3274, 3923, 23434, 12983, 10293]
        for i in ind[0]:
            feature_rec.append(Movie.objects.filter(title=y[i]).first())
        print("rec done complete")

        # dist, ind = model_actor.kneighbors([actor_preference], n_neighbors=12)
        # for i in ind[0]:
        #     actor_rec.append(Movie.objects.filter(title=y[i]).first())

    context_dictionary = {
        "trending_movies": trending_movies,
        "feature_movies": feature_rec,
        "actor_movies": actor_rec
    }
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