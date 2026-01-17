import os
import requests

URL = os.environ.get("M3U_URL")
OUTPUT = "Ayna-cl.m3u"

if not URL:
    raise RuntimeError("M3U_URL secret not found")

r = requests.get(URL, stream=True, timeout=30)
r.raise_for_status()

with open(OUTPUT, "wb") as f:
    for chunk in r.iter_content(8192):
        if chunk:
            f.write(chunk)

print("M3U saved:", OUTPUT)
