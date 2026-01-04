import requests
import re
from collections import defaultdict

# 🔗 GitHub RAW m3u URL
M3U_URL = "https://raw.githubusercontent.com/USERNAME/REPO/main/input.m3u"

# 📁 Output file
OUTPUT_FILE = "output_sorted.m3u"

# 🎯 Group priority order
PRIORITY_GROUPS = ["Bangla", "News", "Sports", "Chanels"]

print("📥 Fetching M3U from GitHub RAW...")

res = requests.get(M3U_URL, timeout=20)
res.raise_for_status()

lines = res.text.splitlines()

groups = defaultdict(list)
current_extinf = None
current_group = "Others"

for line in lines:
    if line.startswith("#EXTINF"):
        current_extinf = line
        match = re.search(r'group-title="([^"]+)"', line)
        current_group = match.group(1) if match else "Others"

    elif line.strip().startswith("http"):
        groups[current_group].append((current_extinf, line))

print("🧠 Sorting group titles...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    # 🔝 Priority groups first
    for grp in PRIORITY_GROUPS:
        for extinf, url in groups.get(grp, []):
            f.write(extinf + "\n")
            f.write(url + "\n")

    # 🔽 All remaining groups (unchanged)
    for grp, items in groups.items():
        if grp not in PRIORITY_GROUPS:
            for extinf, url in items:
                f.write(extinf + "\n")
                f.write(url + "\n")

print("✅ DONE")
print("📂 New M3U created:", OUTPUT_FILE)
