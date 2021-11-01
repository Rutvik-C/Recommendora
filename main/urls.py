from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="app_home"),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="logout"),

]
