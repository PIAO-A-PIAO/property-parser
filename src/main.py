import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from fetcher import fetch_all_pages
from searcher import select_autocomplete_option
from gui import log_message, show_loading_message, show_completion_screen, close_gui

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
            log_message(f"✅ Found installed browser: {name} at {path}")
            return name, path
    log_message("⚠️ No mainstream browser found.")
    return None, None

def install_playwright_browsers():
    log_message("⬇️ Running 'playwright install' to download browsers...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        log_message("✅ Playwright browsers installed successfully.")
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Failed to install browsers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Show initial loading screen
    show_loading_message("Initializing Property Parser...")
    log_message("🚀 Starting Property Parser")
    
    browser_name, browser_executable = find_installed_browser()

    if browser_executable is None:
        # No installed browser found, run playwright install first
        install_playwright_browsers()

    show_loading_message("Setting up browser environment...")
    log_message("🔧 Configuring browser settings")
    
    with sync_playwright() as p:
        if browser_executable:
            log_message(f"Launching installed browser '{browser_name}' at: {browser_executable}")
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
            log_message("⬇️ Launching default Chromium from Playwright...")
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

        show_loading_message("Ready to start! Opening property search...")
        log_message("🌐 Browser ready, starting property search")

        final_url = select_autocomplete_option(context)
        log_message(f"🔗 Final search results URL: {final_url}")

        if final_url:
            show_loading_message("Fetching property listings...")
            log_message("📊 Starting data collection from search results")
            fetch_all_pages(final_url, context)
            
            show_loading_message("Data collection complete! Processing results...")
            log_message("✅ Property data collection finished successfully")
            
            import time
            time.sleep(3)  # Give user time to see completion message
        else:
            log_message("❌ No search URL obtained - process cancelled")

        log_message("🧹 Cleaning up browser resources")
        context.close()
        browser.close()
        
        log_message("🎉 Property Parser completed successfully!")
        
        # Show completion screen with finish button
        show_completion_screen()
