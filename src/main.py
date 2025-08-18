import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from fetcher import fetch_all_pages
from searcher import select_autocomplete_option
from gui import log_message, show_loading_message, show_completion_screen, close_gui
from playwright.async_api import async_playwright
import asyncio

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

async def main():
    show_loading_message("Initializing Property Parser...")
    log_message("🚀 Starting Property Parser")
    
    browser_name, browser_executable = find_installed_browser()

    if browser_executable is None:
        install_playwright_browsers()

    show_loading_message("Setting up browser environment...")
    log_message("🔧 Configuring browser settings")
    
    async with async_playwright() as p:
        if browser_executable:
            log_message(f"Launching installed browser '{browser_name}' at: {browser_executable}")
            if browser_name == "firefox":
                browser = await p.firefox.launch(
                    executable_path=browser_executable,
                    headless=False,
                    args=["--window-position=-10000,-10000"],
                )
                context = await browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    extra_http_headers={
                        # your headers here
                    }
                )
            else:
                # Chromium-based browsers, launch persistent context
                context = await p.chromium.launch_persistent_context(
                    user_data_dir="./src/loopnet_profile",
                    executable_path=browser_executable,
                    headless=False,
                    args=["--window-position=-10000,-10000"],
                    viewport={"width": 1280, "height": 720},
                    extra_http_headers={
                        # your headers here
                    }
                )
        else:
            log_message("⬇️ Launching default Chromium from Playwright...")
            context = await p.chromium.launch_persistent_context(
                user_data_dir="./src/loopnet_profile",
                headless=False,
                args=["--window-position=-10000,-10000"],
                viewport={"width": 1280, "height": 720},
                extra_http_headers={
                    # your headers here
                }
            )

        show_loading_message("Ready to start! Opening property search...")
        log_message("🌐 Browser ready, starting property search")

        final_url = await select_autocomplete_option(context)
        log_message(f"🔗 Final search results URL: {final_url}")

        if final_url:
            show_loading_message("Fetching property listings...")
            log_message("📊 Starting data collection from search results")
            await fetch_all_pages(final_url, context)
            
            show_loading_message("Processing results...")
            log_message("✅ Property data collection finished successfully")
            await asyncio.sleep(3)  # Give user time to see completion message
        else:
            log_message("❌ No search URL obtained - process cancelled")

        log_message("🧹 Cleaning up browser resources")
        await context.close()
        if browser_executable and browser_name == "firefox":
            await browser.close()
        
        log_message("🎉 Property Parser completed successfully!")
        show_completion_screen()

if __name__ == "__main__":
    asyncio.run(main())