from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home_page(request):
    return render(request, "main/index.html")


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