from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home_view(request: HttpRequest):
    return render(
        request,
        "account/home.html",
    )
