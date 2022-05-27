from django.http import *
from django.shortcuts import render, redirect
from .api import valid_filetypes
from django.contrib.auth.decorators import login_required

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


def home_view(request: HttpRequest):
    return render(
        request,
        "home.html",
    )


@login_required
def download_view(request: HttpRequest):
    return render(
        request,
        "download.html",
        context={
            "platforms": platforms.items(),
            "types": types,
            "resolutions": resolutions
        }
    )


@login_required
def shazam_view(request: HttpRequest):
    valid_types = ", ".join([i.upper() for i in valid_filetypes[:-1]])+f" or {valid_filetypes[-1].upper()} (MAX. 8mb)."

    return render(
        request,
        "shazam.html",
        context={
            "valid_types": valid_types
        }
    )


@login_required
def effects_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("/login")

    valid_types = valid_video_types+valid_audio_types
    valid_types = ", ".join([i.upper() for i in valid_types[:-1]])+f" or {valid_types[-1].upper()} (MAX. 8mb)."

    return render(
        request,
        "effects.html",
        context={
            "valid_types": valid_types,
            "effects": effects.items(),
            "audio_types": ",".join(valid_audio_types),
            "video_types": ",".join(valid_video_types)
        }
    )
