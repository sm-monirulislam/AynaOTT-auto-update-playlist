import os
import requests

URL = os.environ.get("M3U_URL")
OUTPUT = "Ayna-cl.m3u"

if not URL:
    raise RuntimeError("M3U_URL secret not found")

r = requests.get(URL, timeout=30)
r.raise_for_status()

lines = r.text.splitlines()

clean = []
extm3u_added = False

for line in lines:
    line = line.strip()

    # Keep only one EXTM3U
    if line == "#EXTM3U":
        if not extm3u_added:
            clean.append("#EXTM3U")
            extm3u_added = True
        continue

    # KEEP EXTINF (title, logo, group)
    if line.startswith("#EXTINF"):
        clean.append(line)
        continue

    # REMOVE other comments
    if line.startswith("#"):
        continue

    # KEEP stream URLs
    if line:
        clean.append(line)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(clean))

print("Playlist updated:", OUTPUT)
