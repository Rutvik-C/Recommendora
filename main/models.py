from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
import json
import pickle
from scipy import sparse
from .utils import *


# Load ML models, feature vectors and other essential objects
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
X_feature_vectors = sparse.load_npz("ml_utils/recommendation/feature_vectors.npz")
X_actor_vectors = sparse.load_npz("ml_utils/recommendation/actor_vectors.npz")
X_director_vectors = sparse.load_npz("ml_utils/recommendation/director_vectors.npz")
X_studio_vectors = sparse.load_npz("ml_utils/recommendation/studio_vectors.npz")


"""
django.contrib.auth.models.User is as follows
ref: django.contrib.auth.models import User

class User:
    id = int()
    username = str()
    email = str()
    password = str()
"""


class Actor(models.Model):
    # id: builtin attribute in django
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_actors(self):
        """
        - Returns list of all actors
        """
        result = []

        for actor in Actor.objects.all():
            result.append(actor.name)

        return result


class Director(models.Model):
    # id: builtin attribute in django
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_directors(self):
        """
        - Returns list of all directors
        """
        result = []

        for director in Director.objects.all():
            result.append(director.name)

        return result


class Genre(models.Model):
    # id: builtin attribute in django
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

    def get_genres(self):
        """
        - Returns list of all genre
        """
        result = []

        for genre in Genre.objects.all():
            result.append(genre.type)

        return result


class Movie(models.Model):
    # id: builtin attribute in django
    title = models.CharField(max_length=200)
    image_url = models.CharField(max_length=250)
    trailer_link = models.CharField(max_length=50)
    year = models.CharField(max_length=15)
    duration = models.CharField(max_length=20)
    language = models.CharField(max_length=200)
    description = models.CharField(max_length=450)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    production_company = models.CharField(max_length=150)
    actors = models.ManyToManyField(Actor)
    directors = models.ManyToManyField(Director)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

    def search_movie(self, movie_name, actor, director, production_studio, language, genre):
        """
        - Return set of movies that fit in the filters set by user
        """
        result = None
        print(actor, director, production_studio, language, genre)

        if movie_name != "":
            _movie = Movie.objects.filter(title__icontains=movie_name)
            result = set(_movie)

        if actor != "":
            _actor = Actor.objects.filter(name=actor).first()
            temp_dir = set(_actor.movie_set.all())
            if result is None:
                result = temp_dir
            else:
                result = result.intersection(temp_dir)

        if director != "":
            _director = Director.objects.filter(name=director).first()
            temp_dir = set(_director.movie_set.all())
            if result is None:
                result = temp_dir
            else:
                result = result.intersection(temp_dir)

        if production_studio != "":
            temp_studio = set(Movie.objects.filter(production_company__contains=production_studio))
            if result is None:
                result = temp_studio
            else:
                result = result.intersection(temp_studio)

        if language != "":
            temp_lang = set(Movie.objects.filter(language__contains=language))
            if result is None:
                result = temp_lang
            else:
                result = result.intersection(temp_lang)

        if genre != "":
            temp_genre = set()
            for g in genre:
                _genre = Genre.objects.filter(type=g).first()
                temp_genre = temp_genre.union(set(_genre.movie_set.all()))

            if result is None:
                result = temp_genre
            else:
                result = result.intersection(temp_genre)

        return result

    def get_movie_recommendation(self):
        """
        - Load recommendations for the current movie
        """
        feature_rec, actor_rec, director_rec, studio_rec = [], [], [], []

        y = data["title"]
        dist, ind = model_feature.kneighbors(X_feature_vectors[self.id], n_neighbors=8)  # Feature based recommendations
        for i in ind[0]:
            feature_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_actor.kneighbors(X_actor_vectors[self.id], n_neighbors=8)  # Actor based recommendations
        for i in ind[0]:
            actor_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_director.kneighbors(X_director_vectors[self.id], n_neighbors=8)  # Director based recommendations
        for i in ind[0]:
            director_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_studio.kneighbors(X_studio_vectors[self.id], n_neighbors=8)  # Studio based recommendations
        for i in ind[0]:
            studio_rec.append(Movie.objects.filter(title=y[i]).first())

        return feature_rec, actor_rec, director_rec, studio_rec

    def get_movies(self):
        """
        - Returns list of all movies, languages, and studio
        """
        result_movie = []
        result_language = set()
        result_studio = set()

        for movie in Movie.objects.all():
            result_movie.append(movie.title)
            for lang in movie.language.split(","):
                result_language.add(lang.strip())
            for studio in movie.production_company.split(","):
                result_studio.add(studio.strip())

        result_language = list(result_language)
        result_language.sort()
        result_studio = list(result_studio)
        result_studio.sort()

        return result_movie, result_language, result_studio


class AuthorizedUser(models.Model):
    # To be implemented with 'History and Liked items'
    # liked_items = []
    # history = []
    feature_preference = models.TextField()
    actor_preference = models.TextField()
    director_preference = models.TextField()
    studio_preference = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def view_history(self):
        """
        - Display users' history
        """
        # To be implemented with 'History and Liked items'
        pass

    def view_liked(self):
        """
        - Display users' liked items
        """
        # To be implemented with 'History and Liked items'
        pass

    def unlike_item(self):
        """
        - Remove a movie from users' liked item list
        """
        # To be implemented with 'History and Liked items'
        pass

    def update_profile(self):
        """
        - Update user profile
        """
        # To be implemented with 'History and Liked items'
        # username, email, password inherited from user class
        pass

    def get_personalized_recommendations(self):
        """
        - Recommend movies based on users' preferences
        """
        feature_rec, actor_rec, director_rec, studio_rec = [], [], [], []

        y = data["title"]
        dist, ind = model_feature.kneighbors([json.loads(self.feature_preference)], n_neighbors=8)  # Based on users feature preference
        for i in ind[0]:
            feature_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_actor.kneighbors([json.loads(self.actor_preference)], n_neighbors=8)  # Based on users actor preference
        for i in ind[0]:
            actor_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_director.kneighbors([json.loads(self.director_preference)], n_neighbors=8)  # Based on users director preference
        for i in ind[0]:
            director_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_studio.kneighbors([json.loads(self.studio_preference)], n_neighbors=8)  # Based on users studio preference
        for i in ind[0]:
            studio_rec.append(Movie.objects.filter(title=y[i]).first())

        return feature_rec, actor_rec, director_rec, studio_rec


class AnonymousUser:
    def register(self, request, username, email, password):
        """
        - Create a new user object
        """
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        authorized_user = AuthorizedUser(
            user=new_user,
            feature_preference=defaults["feature"],
            actor_preference=defaults["actor"],
            director_preference=defaults["director"],
            studio_preference=defaults["studio"]
        )
        authorized_user.save()

        send_email(email, "Welcome to Recommendora!",
                   f"Hey {username},\n\nThanks for joining us.\nYour account has been successfully created. You can now enjoy all our benefits like personalized recommendations, friends activity and many more... Log in to get started\n\nBest,\nTeam Recommendora")
        login(request, new_user)

        return redirect("app_home")

    def login(self, request, username, password):
        """
        - Authorize the user with username and password
        """
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("app_home")

        else:
            messages.success(request, "Invalid credentials")
            return redirect("login")

