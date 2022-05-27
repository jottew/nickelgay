import subprocess

proc = subprocess.Popen("uvicorn nickelgay.asgi:application --reload --port 8000 --host 0.0.0.0".split())
proc.wait()
proc.communicate()
