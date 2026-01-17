import os
import requests

URL = os.environ.get("M3U_URL")
OUTPUT = "Ayna-cl.m3u"

if not URL:
    raise RuntimeError("M3U_URL secret not found")

r = requests.get(URL, timeout=30)
r.raise_for_status()

lines = r.text.splitlines()

clean_lines = []
extm3u_added = False

for line in lines:
    line = line.strip()

    # শুধু একবার #EXTM3U রাখবে
    if line == "#EXTM3U" and not extm3u_added:
        clean_lines.append("#EXTM3U")
        extm3u_added = True
        continue

    # অন্য সব comment বাদ
    if line.startswith("#"):
        continue

    # channel / url lines রাখবে
    if line:
        clean_lines.append(line)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(clean_lines))

print("Clean playlist saved:", OUTPUT)
