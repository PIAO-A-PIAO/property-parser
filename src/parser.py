from bs4 import BeautifulSoup
import csv

def parse_articles_from_string(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article", class_="placard")

    listings = []
    for art in articles:
        listing_id = art.get("data-id", "").strip()

        # Best a_tag with text (Address + Title)
        a_tag = art.select_one("header h4 a")
        url = a_tag["href"].strip() if a_tag and a_tag.has_attr("href") else ""
        address = a_tag.text.strip() if a_tag else ""
        title = a_tag["title"].strip() if a_tag and a_tag.has_attr("title") else ""

        # Location (e.g. City + Zip)
        subtitle_tag = art.select_one("header .subtitle-beta")
        location = subtitle_tag.text.strip() if subtitle_tag else ""

        # Company name
        company_tag = art.select_one(".company-logos li.company-name p")
        company = company_tag.text.strip() if company_tag else ""

        # Price, Cap Rate, Size
        data_points = art.select("ul.data-points-2c li")

        price_element = art.select_one('ul.data-points-2c li[name="Price"]')
        price = price_element.text.strip() if price_element else "upon request"
        size = data_points[1].text.strip() if len(data_points) > 1 else ""
        cap_rate = data_points[0].text.strip() if data_points else ""

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
            "Title": title,
            "Address": address,
            "Location": location,
            "Company": company,
            "Price": price,
            "Cap Rate": cap_rate,
            "Size": size,
            "Images": ";".join(images)
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
    keys = ["Listing ID", "URL", "Title", "Address", "Location", "Company", "Price", "Cap Rate", "Size", "Images"]
    with open(output_csv, mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        if not append:
            writer.writeheader()
        writer.writerows(listings)
