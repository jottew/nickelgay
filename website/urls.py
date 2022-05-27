from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView

from . import views, api, account

urlpatterns = [
    path("", views.home_view),
    path("account/", account.home_view),
    path("shazam/", views.shazam_view),
    path("effects/", views.effects_view),
    path("download/", views.download_view),
    path("api/download/", api.download_view, name="platform"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="login"),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.png"))),
]