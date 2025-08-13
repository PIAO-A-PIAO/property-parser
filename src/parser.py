from bs4 import BeautifulSoup
import csv
import re

def extract_cap_rate_year(text):
    """Extract only the year from 'Built in xxxx' format or return 'upon request'."""
    if not text or text.lower().strip() == "upon request":
        return "upon request"
    
    # Look for year pattern after "Built in"
    match = re.search(r'Built in\s+(\d{4})', text, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # If no year found, return original text
    return text

def extract_numbers_only(text):
    """Extract only numeric values or ranges from text, removing units."""
    if not text or text.lower().strip() == "upon request":
        return "upon request"
    
    # Look for number patterns: individual numbers, ranges, or comma-separated numbers
    number_pattern = r'[\d,]+(?:\.\d+)?'
    range_pattern = rf'{number_pattern}\s*-\s*{number_pattern}'
    
    # First try to find ranges (e.g., "1,000,000 - 2,000,000")
    range_matches = re.findall(range_pattern, text)
    if range_matches:
        return range_matches[0]
    
    # If no ranges, find individual numbers
    number_matches = re.findall(number_pattern, text)
    if number_matches:
        # If multiple numbers found, join them with " / " to preserve the structure
        return " - ".join(number_matches)
    
    # If no numbers found, return original text
    return text

def separate_location_and_postal_code(location_text):
    """Separate location into city/state and postal code."""
    if not location_text:
        return "", ""
    
    # Pattern to match postal code at the end (US/Canada format)
    postal_pattern = r'\s+([A-Za-z]\d[A-Za-z]\s*\d[A-Za-z]\d|\d{5}(?:-\d{4})?)$'
    match = re.search(postal_pattern, location_text)
    
    if match:
        postal_code = match.group(1).strip()
        city_state = location_text[:match.start()].strip()
        return city_state, postal_code
    else:
        # If no postal code found, return original as city_state
        return location_text.strip(), ""

def parse_articles_from_string(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article", class_="placard")

    listings = []
    for art in articles:
        listing_id = art.get("data-id", "").strip()

        # Best a_tag with text (Address)
        a_tag = art.select_one("header h4 a")
        url = a_tag["href"].strip() if a_tag and a_tag.has_attr("href") else ""
        address = a_tag.text.strip() if a_tag else ""

        # Location (e.g. City + Zip)
        # Check if article has "tier2" in class, if so get location from header h6 a
        if "tier2" in art.get("class", []):
            location_tag = art.select_one("header h6 a")
            location_full = location_tag.text.strip() if location_tag else ""
        else:
            subtitle_tag = art.select_one("header .subtitle-beta")
            location_full = subtitle_tag.text.strip() if subtitle_tag else ""
        
        # Separate location into city/state and postal code
        location, postal_code = separate_location_and_postal_code(location_full)

        # Company name
        if "tier2" in art.get("class", []):
            # For tier2 articles, get company from ul.contacts li title
            contact_li = art.select_one("ul.contacts li")
            company = contact_li.get("title", "").strip() if contact_li else ""
        else:
            company_tag = art.select_one(".company-logos li.company-name p")
            if company_tag:
                company = company_tag.text.strip()
            else:
                # Fallback to li.company-logo img alt text
                logo_img = art.select_one(".company-logos li.company-logo img")
                company = logo_img.get("alt", "").strip() if logo_img else ""

        # Price, Cap Rate, Size
        if "tier2" in art.get("class", []):
            # For tier2 articles, extract price and cap_rate from ul.data-points-a
            data_points_a = art.select("ul.data-points-a li")
            
            price = "upon request"
            cap_rate = "upon request"
            
            for li in data_points_a:
                li_text = li.text.strip()
                # Look for price indicator (contains $ or CAD/SF/YR)
                if "$" in li_text or "CAD/SF/YR" in li_text or li.get("name") == "Price":
                    price = extract_numbers_only(li_text)
                # Look for cap rate info (contains "Built in") - only from non-Price elements
                elif "Built in" in li_text and not ("$" in li_text or "CAD/SF/YR" in li_text or li.get("name") == "Price"):
                    cap_rate = extract_cap_rate_year(li_text)
            
            # Size for tier2: always get from header .text-right h4 a
            size_tag = art.select_one("header .text-right h4 a")
            size = extract_numbers_only(size_tag.text.strip()) if size_tag else ""
        else:
            # For non-tier2 articles
            data_points = art.select("ul.data-points-2c li")
            
            price_element = art.select_one('ul.data-points-2c li[name="Price"]')
            price = extract_numbers_only(price_element.text.strip()) if price_element else "upon request"
            
            size = "upon request"
            cap_rate = "upon request"
            
            # Parse data_points to identify size (contains SF) and cap_rate (contains Built in)
            # Exclude Price elements when looking for size and cap_rate
            for li in data_points:
                li_text = li.text.strip()
                # Skip if this is a Price element
                if "$" in li_text or "CAD/SF/YR" in li_text or li.get("name") == "Price":
                    continue
                    
                if "SF" in li_text:
                    size = extract_numbers_only(li_text)
                elif "Built in" in li_text:
                    cap_rate = extract_cap_rate_year(li_text)

        # Image URLs
        images = []
        for figure in art.select("figure"):
            # Try to get background-image from style attribute
            style = figure.get("style", "")
            if "background-image" in style:
                start = style.find("url(")
                end = style.find(")", start)
                if start != -1 and end != -1:
                    images.append(style[start+4:end].strip('"').strip("'"))
            # Else try <img src=...> or lazy-src
            img = figure.find("img")
            if img:
                src = img.get("src") or img.get("lazy-src")
                if src:
                    images.append(src)

        listings.append({
            "Listing ID": listing_id,
            "URL": url,
            "Address": address,
            "Location": location,
            "Postal Code": postal_code,
            "Company": company,
            "Price (CAD/SF/Year)": price,
            "Cap Rate": cap_rate,
<<<<<<< HEAD
            "Size": size,
=======
            "Size (SF)": size,
>>>>>>> origin/dev
            "Images": " | ".join(images)
        })


    return listings

def extract_next_page_url(html):
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.select_one('a[data-automation-id="NextPage"]')
    if next_link and next_link.has_attr("href"):
        return next_link["href"]
    return None

def append_to_csv(listings, output_csv, append=True):
    mode = "a" if append else "w"
    keys = ["Listing ID", "URL", "Address", "Location", "Postal Code", "Company", "Price (CAD/SF/Year)", "Cap Rate", "Size (SF)", "Images"]
    with open(output_csv, mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        if not append:
            writer.writeheader()
        writer.writerows(listings)
