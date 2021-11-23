from django.db import models
from django.contrib.auth.models import User
import json
import pickle
from scipy import sparse


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
X_feature_vectors = sparse.load_npz("ml_utils/recommendation/feature_vectors.npz")
X_actor_vectors = sparse.load_npz("ml_utils/recommendation/actor_vectors.npz")
X_director_vectors = sparse.load_npz("ml_utils/recommendation/director_vectors.npz")
X_studio_vectors = sparse.load_npz("ml_utils/recommendation/studio_vectors.npz")


class Actor(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_actors(self):
        result = []

        for actor in Actor.objects.all():
            result.append(actor.name)

        return result


class Director(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_directors(self):
        result = []

        for director in Director.objects.all():
            result.append(director.name)

        return result


class Genre(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

    def get_genres(self):
        result = []

        for genre in Genre.objects.all():
            result.append(genre.type)

        return result


class Movie(models.Model):
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

    def search_movie(self, actor, director, production_studio, language, genre):
        result = None
        print(actor, director, production_studio, language, genre)

        if actor != "":
            _actor = Actor.objects.filter(name=actor).first()
            result = set(_actor.movie_set.all())

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
        feature_rec, actor_rec, director_rec, studio_rec = [], [], [], []

        y = data["title"]
        dist, ind = model_feature.kneighbors(X_feature_vectors[self.id], n_neighbors=8)
        for i in ind[0]:
            feature_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_actor.kneighbors(X_actor_vectors[self.id], n_neighbors=8)
        for i in ind[0]:
            actor_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_director.kneighbors(X_director_vectors[self.id], n_neighbors=8)
        for i in ind[0]:
            director_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_studio.kneighbors(X_studio_vectors[self.id], n_neighbors=8)
        for i in ind[0]:
            studio_rec.append(Movie.objects.filter(title=y[i]).first())

        return feature_rec, actor_rec, director_rec, studio_rec

    def get_movies(self):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    feature_preference = models.TextField()
    actor_preference = models.TextField()
    director_preference = models.TextField()
    studio_preference = models.TextField()

    def get_personalized_recommendations(self):
        feature_rec, actor_rec, director_rec, studio_rec = [], [], [], []

        y = data["title"]
        dist, ind = model_feature.kneighbors([json.loads(self.feature_preference)], n_neighbors=8)
        for i in ind[0]:
            feature_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_actor.kneighbors([json.loads(self.actor_preference)], n_neighbors=8)
        for i in ind[0]:
            actor_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_director.kneighbors([json.loads(self.director_preference)], n_neighbors=8)
        for i in ind[0]:
            director_rec.append(Movie.objects.filter(title=y[i]).first())

        dist, ind = model_studio.kneighbors([json.loads(self.studio_preference)], n_neighbors=8)
        for i in ind[0]:
            studio_rec.append(Movie.objects.filter(title=y[i]).first())

        return feature_rec, actor_rec, director_rec, studio_rec
