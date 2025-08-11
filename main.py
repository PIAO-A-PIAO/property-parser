from fetcher import fetch_all_pages
from searcher import select_autocomplete_option

if __name__ == "__main__":
    profile_path = "playwright_profile"  # fixed user data dir for Playwright

    # Pass the keyword and profile_path to the searcher function
    final_url = select_autocomplete_option(user_data_dir=profile_path)

    print(f"\n🔗 Final search results URL: {final_url}")

    if final_url:
        fetch_all_pages(final_url, profile_path)
