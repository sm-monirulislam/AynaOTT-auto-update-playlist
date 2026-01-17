import os
import requests
import re

URL = os.environ.get("M3U_URL")
OUTPUT = "Ayna-cl.m3u"

if not URL:
    raise RuntimeError("M3U_URL secret not found")

r = requests.get(URL, timeout=30)
r.raise_for_status()

lines = r.text.splitlines()

clean = []
extm3u_added = False

seen_urls = set()
seen_names = set()

current_extinf = None
current_name = None

def extract_name(extinf_line: str):
    # channel name = last part after comma
    if "," in extinf_line:
        return extinf_line.split(",", 1)[1].strip().lower()
    return None

for line in lines:
    line = line.strip()

    # Keep single EXTM3U
    if line == "#EXTM3U":
        if not extm3u_added:
            clean.append("#EXTM3U")
            extm3u_added = True
        continue

    # EXTINF (metadata)
    if line.startswith("#EXTINF"):
        current_extinf = line
        current_name = extract_name(line)
        continue

    # Remove other comments
    if line.startswith("#"):
        continue

    # Stream URL
    if line and current_extinf:
        url_key = line.lower()

        # Duplicate check (by URL or channel name)
        if url_key in seen_urls or (current_name and current_name in seen_names):
            current_extinf = None
            current_name = None
            continue

        # Save unique channel
        seen_urls.add(url_key)
        if current_name:
            seen_names.add(current_name)

        clean.append(current_extinf)
        clean.append(line)

        current_extinf = None
        current_name = None

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(clean))

print("Playlist updated (duplicates removed):", OUTPUT)
