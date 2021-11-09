from .models import *


def get_all_movie_info():
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


def get_all_genre():
    result = []

    for genre in Genre.objects.all():
        result.append(genre.type)

    return result


def get_all_actor():
    result = []

    for actor in Actor.objects.all():
        result.append(actor.name)

    return result


def get_all_director():
    result = []

    for director in Director.objects.all():
        result.append(director.name)

    return result
