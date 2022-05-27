import json

from django.http import *
from django.shortcuts import render
from .api import valid_filetypes
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext, activate, get_language_info

platforms = {
    "YouTube": "YouTube",
    "TikTok": "TikTok",
    "Twitter": "Twitter",
    "Reddit": "Reddit",
    "SoundCloud": "SoundCloud",
    "Roblox Songs": "Roblox"
}

types = [
    "Video",
    "Audio"
]

resolutions = [
    "2160",
    "1440",
    "1080",
    "720",
    "480",
    "360",
    "240",
    "144"
]

effects = {
    "nightcore": "Nightcore",
    "loud": "Loud",
    "earrape": "Earrape",
    "lnc": "Loud Nightcore",
    "ncer": "Earrape Nightcore",
}

valid_video_types = [
    "mp4",
    "webm",
    "m4v",
    "mkv",
    "flv",
    "avi"
]

valid_audio_types = [
    "mp3",
    "ogg",
    "wav",
    "aac"
]

"""
authenticated:
    True: specifically is authenticated
    False: specifically is not authenticated
    None: doesn't matter
"""
nav = {
    "../": {
        "admin": False,
        "authenticated": None,
        "name": gettext("Home")
    },
    "/download/": {
        "admin": False,
        "authenticated": None,
        "name": gettext("Download")
    },
    "/shazam/": {
        "admin": False,
        "authenticated": None,
        "name": gettext("Shazam")
    },
    "/effects/": {
        "admin": False,
        "authenticated": None,
        "name": gettext("Effects")
    },
    "/admin/": {
        "admin": True,
        "authenticated": True,
        "name": gettext("Admin")
    },
    "/login/": {
        "admin": False,
        "authenticated": False,
        "name": gettext("Login")
    },
    "/logout/": {
        "admin": False,
        "authenticated": True,
        "name": gettext("Logout")
    },
}


def create_nav(request: HttpRequest):
    new_nav = nav.copy()

    admin = [k for k, v in new_nav.items() if v["admin"]]
    authenticated = [k for k, v in new_nav.items() if v["authenticated"] is True]
    not_authenticated = [k for k, v in new_nav.items() if v["authenticated"] is False]

    if not request.user.is_staff:
        for i in admin:
            try:
                new_nav.pop(i)
            except Exception:
                pass

    if not request.user.is_authenticated:
        for i in authenticated:
            try:
                new_nav.pop(i)
            except Exception:
                pass

    if request.user.is_authenticated:
        for i in not_authenticated:
            try:
                new_nav.pop(i)
            except Exception:
                pass

    navs = dict([(v["name"], k) for k, v in new_nav.items()])

    return navs.items()


def home_view(request: HttpRequest):
    new_nav = create_nav(request)

    return render(
        request,
        "home.html",
        context={
            "nav": new_nav
        }
    )


@login_required
def download_view(request: HttpRequest):
    new_nav = create_nav(request)

    return render(
        request,
        "download.html",
        context={
            "platforms": platforms.items(),
            "types": types,
            "resolutions": resolutions,
            "nav": new_nav
        }
    )


@login_required
def shazam_view(request: HttpRequest):
    new_nav = create_nav(request)
    valid_types = ", ".join([i.upper() for i in valid_filetypes[:-1]])+f" or {valid_filetypes[-1].upper()} (MAX. 8mb)."

    return render(
        request,
        "shazam.html",
        context={
            "valid_types": valid_types,
            "nav": new_nav
        }
    )


@login_required
def effects_view(request: HttpRequest):
    new_nav = create_nav(request)
    valid_types = valid_video_types+valid_audio_types
    valid_types = ", ".join([i.upper() for i in valid_types[:-1]])+f" or {valid_types[-1].upper()} (MAX. 8mb)."

    return render(
        request,
        "effects.html",
        context={
            "valid_types": valid_types,
            "effects": effects.items(),
            "audio_types": ",".join(valid_audio_types),
            "video_types": ",".join(valid_video_types),
            "nav": new_nav
        }
    )
