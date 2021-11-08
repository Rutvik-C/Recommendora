from .models import *


def get_all_movies():
    result = []

    for movie in Movie.objects.all():
        result.append(movie.title)

    return result
