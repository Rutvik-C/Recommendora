from django.shortcuts import render
from django.core.mail import send_mail


def not_found_404(request):
    """
    - Display a custom 404 page
    """
    response = render(request, "main/404.html")
    response.status_code = 404
    return response


def send_email(email, subject, message):
    """
    - Send email to user
    """
    send_mail(
        subject=subject,
        message=message,
        from_email="recommendora@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )
