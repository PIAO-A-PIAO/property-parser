import urllib.request
import zipfile
import io
import os
import shutil
import sys
import time

UPDATE_ZIP_URL = "https://github.com/PIAO-A-PIAO/property-parser/archive/refs/heads/main.zip"
VERSIONS_URL = "https://raw.githubusercontent.com/PIAO-A-PIAO/property-parser/main/versions.txt"
LOCAL_VERSION_FILE = "versions.txt"


def get_remote_version_info():
    with urllib.request.urlopen(VERSIONS_URL) as response:
        lines = response.read().decode().splitlines()
        return lines[-1].strip()  # Return full latest line


def parse_version_line(line):
    """Split '1.2.0: something' into ('1.2.0', 'something')"""
    if ":" in line:
        version, desc = line.split(":", 1)
        return version.strip(), desc.strip()
    return line.strip(), ""


def get_local_version_line():
    try:
        with open(LOCAL_VERSION_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0: (no local version)"


def save_local_version_line(version_line):
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(version_line)


def version_to_tuple(v):
    return tuple(int(x) for x in v.split("."))


def is_update_available(compare_full_line=False):
    remote_line = get_remote_version_info()
    local_line = get_local_version_line()

    if compare_full_line:
        return remote_line != local_line
    else:
        remote_version, _ = parse_version_line(remote_line)
        local_version, _ = parse_version_line(local_line)
        return version_to_tuple(remote_version) > version_to_tuple(local_version)


def download_and_extract_update(zip_url, extract_to="."):
    print("⬇️ Downloading update archive...")
    with urllib.request.urlopen(zip_url) as response:
        data = response.read()

    print("📦 Extracting files...")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        temp_extract_path = os.path.join(extract_to, "_temp_update")
        if os.path.exists(temp_extract_path):
            shutil.rmtree(temp_extract_path)
        z.extractall(temp_extract_path)

        # GitHub ZIP usually contains a root folder; get it
        root_folder = next(os.scandir(temp_extract_path)).path

        # Move files from root_folder to extract_to, overwrite existing
        for root, dirs, files in os.walk(root_folder):
            rel_path = os.path.relpath(root, root_folder)
            target_dir = os.path.join(extract_to, rel_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                print(f"➡️ Updating {dst_file}")
                shutil.move(src_file, dst_file)

        # Clean up temp folder
        shutil.rmtree(temp_extract_path)
        
if __name__ == "__main__":
    if is_update_available(compare_full_line=False):
        try:
            remote_line = get_remote_version_info()
            version, desc = parse_version_line(remote_line)
            print(f"🔔 New version {version} available: {desc}")

            download_and_extract_update(UPDATE_ZIP_URL)
            save_local_version_line(remote_line)
            print("✅ Update completed successfully.")

            print("🔄 Restarting to apply update...")
            time.sleep(1)
            os.execv(sys.executable, ['python'] + sys.argv)

        except Exception as e:
            print(f"❌ Update failed: {e}")
            print("Continuing with the current version...")

    else:
        print("✅ You’re up to date.")
