from parser import parse_articles_from_string, extract_next_page_url, append_to_csv
import time

def fetch_all_pages(url, context, output_csv="parsed_listings.csv"):
    page = context.new_page()

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
    
    page.close()
