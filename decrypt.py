import pyzipper
import os

ZIP_FILES = [
    "sm_ayna.zip",
    "sm_ayna_main.zip"
]

EXTRACT_BASE = "extracted"

def decrypt_zip(zip_file):
    password = os.getenv("ZIP_PASSWORD")
    if not password:
        raise ValueError("❌ ZIP_PASSWORD secret not found!")

    password_bytes = password.encode("utf-8")

    extract_folder = os.path.join(EXTRACT_BASE, zip_file.replace(".zip", ""))

    print(f"🔐 Extracting {zip_file} ...")

    os.makedirs(extract_folder, exist_ok=True)

    with pyzipper.AESZipFile(zip_file) as zf:
        zf.pwd = password_bytes
        zf.extractall(extract_folder)

    print(f"📂 Extracted to: {extract_folder}")

    # Extracted ফাইলগুলো root folder এ কপি
    for f in os.listdir(extract_folder):
        src = os.path.join(extract_folder, f)
        dst = os.path.join(".", f)

        if os.path.isfile(src):
            with open(src, "rb") as s, open(dst, "wb") as d:
                d.write(s.read())

    print(f"✅ {zip_file} done\n")


if __name__ == "__main__":
    for zip_file in ZIP_FILES:
        if os.path.exists(zip_file):
            decrypt_zip(zip_file)
        else:
            print(f"⚠️ File not found: {zip_file}")
