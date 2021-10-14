from django.shortcuts import render


def login(request):
    return render(request, "authenticate/login.html")


def register(request):
    return render(request, "authenticate/register.html")
