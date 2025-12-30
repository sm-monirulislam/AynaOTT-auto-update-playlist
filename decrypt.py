import pyzipper
import os

ZIP_FILE = "sm_ayna.zip"      # 🔁 main.zip → sm_ayna.zip
EXTRACT_FOLDER = "extracted"

def decrypt_zip():
    password = os.getenv("ZIP_PASSWORD")
    if not password:
        raise ValueError("❌ ZIP_PASSWORD secret not found!")

    password_bytes = password.encode("utf-8")

    print("🔐 Extracting ZIP...")

    if not os.path.exists(EXTRACT_FOLDER):
        os.makedirs(EXTRACT_FOLDER)

    with pyzipper.AESZipFile(ZIP_FILE) as zf:
        zf.pwd = password_bytes
        zf.extractall(EXTRACT_FOLDER)

    print("📂 Extracted to:", EXTRACT_FOLDER)

    # Extracted ফাইলগুলো root folder এ কপি
    for f in os.listdir(EXTRACT_FOLDER):
        src = os.path.join(EXTRACT_FOLDER, f)
        dst = os.path.join(".", f)
        if os.path.isfile(src):
            with open(src, "rb") as s, open(dst, "wb") as d:
                d.write(s.read())

    print("🎉 Decrypt & unzip done successfully!")

if __name__ == "__main__":
    decrypt_zip()
