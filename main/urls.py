from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="app_home"),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("search_movie/", views.search_movie, name="search_movie"),
    path("movie_info/", views.movie_information, name="movie_info"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("user_rate/", views.user_rate, name="user_rate"),
    path("user_favorite/", views.user_favorite, name="user_favorite"),
]
