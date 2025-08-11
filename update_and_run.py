import urllib.request

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

def is_update_available(compare_full_line=False):
    remote_line = get_remote_version_info()
    local_line = get_local_version_line()

    if compare_full_line:
        return remote_line != local_line
    else:
        remote_version, _ = parse_version_line(remote_line)
        local_version, _ = parse_version_line(local_line)
        return remote_version != local_version

# === Example usage ===
if is_update_available(compare_full_line=False):  # Change to True if you want full line comparison
    remote_line = get_remote_version_info()
    version, desc = parse_version_line(remote_line)
    print(f"🔔 New version {version} available: {desc}")
    # TODO: Download and replace main.py
    save_local_version_line(remote_line)
else:
    print("✅ You’re up to date.")
