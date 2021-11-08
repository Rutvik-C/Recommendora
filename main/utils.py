from .models import *


def get_all_movies():
    result = []

    for movie in Movie.objects.all():
        result.append(movie.title)

    return result


def get_all_genre():
    result = []

    for genre in Genre.objects.all():
        result.append(genre.type)

    return result
