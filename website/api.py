import os
import random
import shutil
import string

import aiofiles
import asyncio

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
import mimetypes

valid_filetypes = [
        "mp4",
        "mp3",
        "mov"
    ]


async def shell(code):
    proc = await asyncio.create_subprocess_shell(
        code,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    return stdout.decode(), stderr.decode()


@login_required
async def download_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponse("Not logged in", status=403)

    args = [
        "platform",
        "url",
        "name",
        "type"
    ]

    for arg in args:
        if not request.GET.get(arg):
            return HttpResponse(f"\"{arg}\" argument missing", status=406)

    platform = request.GET.get("platform")
    url = request.GET.get("url")
    name = request.GET.get("name")
    filetype = request.GET.get("type")

    async with aiofiles.tempfile.TemporaryDirectory() as d:
        name = name or "".join(random.choices(string.ascii_letters+string.digits, k=16))
        path = os.path.join(d, f"{name}.{filetype}")
        code = f"yt-dlp --output \"{path}\" -S vcodec:h264 {url}"

    filepath = "static/nickel.txt"
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = f"attachment; filename={filepath.split('/')[-1]}"
    return response
