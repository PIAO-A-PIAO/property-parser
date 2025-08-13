import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from fetcher import fetch_all_pages
from searcher import select_autocomplete_option

# === Common system paths for various browsers ===
BROWSER_PATHS = {
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
}

def find_installed_browser():
    for name, path in BROWSER_PATHS.items():
        if Path(path).is_file():
            print(f"✅ Found installed browser: {name} at {path}")
            return name, path
    print("⚠️ No mainstream browser found.")
    return None, None

def install_playwright_browsers():
    print("⬇️ Running 'playwright install' to download browsers...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        print("✅ Playwright browsers installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install browsers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    browser_name, browser_executable = find_installed_browser()

    if browser_executable is None:
        # No installed browser found, run playwright install first
        install_playwright_browsers()

    with sync_playwright() as p:
        if browser_executable:
            print(f"Launching installed browser '{browser_name}' at: {browser_executable}")
            if browser_name == "firefox":
                browser = p.firefox.launch(
                    executable_path=browser_executable,
                    headless=False,
                    args=["--window-position=-10000,-10000"],
                )
            else:
                browser = p.chromium.launch(
                    executable_path=browser_executable,
                    headless=False,
                    args=["--window-position=-10000,-10000"],
                )
        else:
            print("⬇️ Launching default Chromium from Playwright...")
            browser = p.chromium.launch(
                headless=False,
                args=["--window-position=-10000,-10000"],
            )

        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            extra_http_headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Cache-Control": "max-age=0"
            }
        )

        final_url = select_autocomplete_option(context)
        print(f"\n🔗 Final search results URL: {final_url}")

        if final_url:
            fetch_all_pages(final_url, context)

        context.close()
        browser.close()
