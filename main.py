from playwright.sync_api import sync_playwright
from fetcher import fetch_all_pages
from searcher import select_autocomplete_option

if __name__ == "__main__":
    profile_path = "playwright_profile"  # fixed user data dir for Playwright

    with sync_playwright() as p:
        # Create a single browser context to be shared
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=False,
            viewport={"width": 1280, "height": 720},
            args=[
                "--window-position=-10000,-10000"
            ],
        )
        
        # Pass the context to the searcher function
        final_url = select_autocomplete_option(context)

        print(f"\n🔗 Final search results URL: {final_url}")

        if final_url:
            fetch_all_pages(final_url, context)
        
        context.close()
