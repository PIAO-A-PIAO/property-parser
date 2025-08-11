from playwright.sync_api import sync_playwright
from parser import parse_articles_from_string, extract_next_page_url, append_to_csv
import os
import time

def fetch_all_pages(url, user_data_dir, output_csv="parsed_listings.csv", headless=False):
    os.makedirs(user_data_dir, exist_ok=True)

    with sync_playwright() as p:
        with p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=headless,
            viewport={"width": 1280, "height": 720},
            args=["--disable-http2", "--disable-quic", "--window-position=-10000,-10000"],
        ) as context:
            page = context.new_page()

            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0.0.0 Safari/537.36"
            })

            current_url = url
            page_num = 1

            while True:
                print(f"\n🟢 Page {page_num}: {current_url}")
                response_html = None
                MAX_RETRIES = 3
                attempt = 0

                while attempt < MAX_RETRIES and not response_html:
                    try:
                        response = page.goto(current_url, wait_until="domcontentloaded", timeout=30000)
                        if response and response.status == 200:
                            response_html = response.text()
                        else:
                            print(f"⚠️ Got status {response.status} on attempt {attempt + 1}")
                    except Exception as e:
                        print(f"⚠️ Attempt {attempt + 1} failed to load {current_url}: {e}")

                    if not response_html:
                        attempt += 1
                        time.sleep(2)

                if not response_html:
                    print("❌ Failed to capture HTML response after retries. Exiting.")
                    break

                listings = parse_articles_from_string(response_html)
                if listings:
                    append_to_csv(listings, output_csv, append=(page_num > 1))
                    print(f"✅ Parsed and added {len(listings)} listings.")
                else:
                    print("⚠️ No listings found on page.")
                    break

                next_url = extract_next_page_url(response_html)
                if next_url:
                    current_url = next_url
                    page_num += 1
                else:
                    print("🔚 No next page found. Done.")
                    break
