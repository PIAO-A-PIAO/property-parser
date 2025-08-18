import asyncio
from parser import parse_articles_from_string, extract_next_page_url, append_to_csv
from gui import log_message
import time
from datetime import datetime

async def fetch_all_pages(url, context, output_csv=None):
    if output_csv is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_csv = f"parsed_listings_{timestamp}.csv"
    
    page = await context.new_page()

    current_url = url
    page_num = 1

    while True:
        log_message(f"🟢 Page {page_num}: {current_url}")
        response_html = None
        MAX_RETRIES = 3
        attempt = 0

        while attempt < MAX_RETRIES and not response_html:
            try:
                response = await page.goto(current_url, wait_until="domcontentloaded", timeout=30000)
                if response and response.status == 200:
                    response_html = await response.text()
                else:
                    log_message(f"⚠️ Got status {response.status} on attempt {attempt + 1}")
            except Exception as e:
                log_message(f"⚠️ Attempt {attempt + 1} failed to load {current_url}: {e}")

            if not response_html:
                attempt += 1
                await asyncio.sleep(2)

        if not response_html:
            log_message("❌ Failed to capture HTML response after retries. Exiting.")
            break

        listings = parse_articles_from_string(response_html)
        if listings:
            append_to_csv(listings, output_csv, append=(page_num > 1))
            log_message(f"✅ Parsed and added {len(listings)} listings.")
        else:
            log_message("⚠️ No listings found on page.")
            break

        next_url = extract_next_page_url(response_html)
        if next_url:
            # Extract the ?sk= parameter from current URL and append to next URL
            if "?sk=" in current_url:
                sk_param = current_url[current_url.find("?sk="):]
                next_url = next_url + sk_param
            current_url = next_url
            page_num += 1
        else:
            log_message("🔚 No next page found. Done.")
            break
    
    await page.close()
