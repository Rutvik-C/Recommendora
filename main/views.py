from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import *
from .utils import *

with open("ml_utils/recommendation/feature_default.json", "r") as f:
    defaults = json.load(f)


_movie = Movie()
_actor = Actor()
_director = Director()
print("[+] Fetching movie info")
movie_names, languages, studio = _movie.get_movies()
all_movies = json.dumps(movie_names)
all_languages = json.dumps(languages)
all_studios = json.dumps(studio)
print("[+] Fetching actor info")
all_actors = json.dumps(_actor.get_actors())
print("[+] Fetching director info")
all_directors = json.dumps(_director.get_directors())


def home_page(request):
    trending_movies = Movie.objects.all().order_by("-views")[:12]

    feature_rec, actor_rec, director_rec, studio_rec = [], [], [], []
    if request.user.is_authenticated:
        authorized_user = AuthorizedUser.objects.get(user=request.user)
        feature_rec, actor_rec, director_rec, studio_rec = authorized_user.get_personalized_recommendations()

    context_dictionary = {
        "trending_movies": trending_movies,
        "feature_movies": feature_rec,
        "actor_movies": actor_rec,
        "director_movies": director_rec,
        "studio_movies": studio_rec,
        "all_movies": all_movies
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

        authorized_user = AuthorizedUser(
            user=new_user,
            feature_preference=defaults["feature"],
            actor_preference=defaults["actor"],
            director_preference=defaults["director"],
            studio_preference=defaults["studio"]
        )
        authorized_user.save()

        send_email(email, "Welcome to Recommendora!", f"Hey {username},\n\nThanks for joining us.\nYour account has been successfully created. You can now enjoy all our benefits like personalized recommendations, friends activity and many more... Log in to get started\n\nBest,\nTeam Recommendora")
        login(request, new_user)
        return redirect("app_home")

    else:
        return render(request, "main/register.html")


def user_logout(request):
    logout(request)
    return redirect("app_home")


def search_movie(request):
    result = None

    if request.method == "POST":
        d = dict(request.POST)
        actor = d["actor"][0]
        director = d["director"][0]
        production_studio = d["studio"][0]
        language = d["language"][0]
        if "genre" in d:
            genre = d["genre"]
        else:
            genre = ""

        movie = Movie()
        result = movie.search_movie(actor, director, production_studio, language, genre)

    if result is None:
        result = []

    _genre = Genre()
    context_dictionary = {
        "all_actors": all_actors,
        "all_directors": all_directors,
        "all_languages": all_languages,
        "all_studios": all_studios,
        "all_movies": all_movies,
        "all_genre": _genre.get_genres(),
        "search_movies": list(result)
    }

    return render(request, 'main/searchmovie.html', context_dictionary)


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


def movie_information(request):
    try:
        if "id" in request.GET:
            movie_id = int(request.GET.get("id"))
            print(movie_id)

            movie = Movie.objects.filter(id=movie_id)
            if len(movie) != 0:
                movie = movie.first()

                if "=" in movie.trailer_link:
                    trailer = movie.trailer_link.split("=")[1]

                else:
                    trailer = "eSIJddEieLI"

                feature_rec, actor_rec, director_rec, studio_rec = movie.get_movie_recommendation()

                context_dict = {
                    "movie": movie,
                    "trailer": trailer,
                    "feature_movies": feature_rec,
                    "actor_movies": actor_rec,
                    "director_movies": director_rec,
                    "studio_movies": studio_rec,
                }

                return render(request, "main/movie.html", context_dict)

        return not_found_404(request)

    except Exception as e:
        print(e)
        return not_found_404(request)


@login_required
def user_rate(request):
    return render(request, 'main/userrate.html')


@login_required
def user_favorite(request):
    return render(request, 'main/userfavorite.html')