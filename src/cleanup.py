import os
import shutil
from pathlib import Path

def cleanup_playwright_and_pycache(project_root=None):
    # Determine project root directory
    if project_root is None:
        project_root = Path(__file__).parent.resolve()

    # 1) Remove all __pycache__ folders recursively
    print("🧹 Cleaning __pycache__ folders...")
    for pycache_dir in project_root.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            print(f"Deleted: {pycache_dir}")
        except Exception as e:
            print(f"⚠️ Failed to delete {pycache_dir}: {e}")

    # 2) Remove Playwright browser downloads directory
    # Default location on Windows is %LOCALAPPDATA%\ms-playwright
    local_appdata = os.getenv("LOCALAPPDATA")
    if local_appdata:
        playwright_dir = Path(local_appdata) / "ms-playwright"
        if playwright_dir.exists():
            try:
                print(f"🧹 Deleting Playwright browsers folder at {playwright_dir} ...")
                shutil.rmtree(playwright_dir)
                print("Playwright browser binaries deleted.")
            except Exception as e:
                print(f"⚠️ Failed to delete Playwright browsers folder: {e}")
        else:
            print(f"No Playwright browsers folder found at {playwright_dir}")
    else:
        print("⚠️ Could not find LOCALAPPDATA environment variable to locate Playwright folder.")

    # 3) Remove local persistent browser profile directory './loopnet_profile'
    loopnet_profile_dir = project_root / "loopnet_profile"
    print(loopnet_profile_dir)
    if loopnet_profile_dir.exists():
        try:
            print(f"🧹 Deleting persistent browser profile folder at {loopnet_profile_dir} ...")
            shutil.rmtree(loopnet_profile_dir)
            print("Persistent browser profile deleted.")
        except Exception as e:
            print(f"⚠️ Failed to delete persistent browser profile folder: {e}")
    else:
        print(f"No persistent browser profile folder found at {loopnet_profile_dir}")

# Example usage
if __name__ == "__main__":
    cleanup_playwright_and_pycache()
