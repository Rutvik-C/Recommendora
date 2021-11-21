from django.shortcuts import render
from django.core.mail import send_mail
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


def not_found_404(request):
    response = render(request, "main/404.html")
    response.status_code = 404
    return response


def send_email(email, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email="recommendora@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )
