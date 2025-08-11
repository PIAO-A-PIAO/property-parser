# Real Estate Scraper

A Python web scraper for LoopNet.ca that allows you to search and extract commercial real estate listings data into a CSV file.

## Features

- Interactive search selection (sale type, property type, location)
- Automated pagination through search results
- Extracts detailed listing information including:
  - Listing ID, URL, Title
  - Address and Location
  - Company name
  - Price, Cap Rate, Size
  - Property images
- Exports data to CSV format
- Retry logic for reliable scraping

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## Usage

Run the main script:
```bash
python main.py
```

The script will guide you through:
1. **Sale Type**: Choose between For Lease, For Sale, or Businesses For Sale
2. **Property Type**: Select from available property categories
3. **Location**: Enter a keyword and select from autocomplete suggestions

The scraper will then automatically:
- Navigate through all result pages
- Extract listing data
- Save to `parsed_listings.csv`

## Output

The CSV file contains the following columns:
- Listing ID
- URL
- Title
- Address
- Location
- Company
- Price
- Cap Rate
- Size
- Images

## Files

- `main.py` - Entry point and orchestration
- `searcher.py` - Interactive search interface
- `fetcher.py` - Web scraping and pagination logic
- `parser.py` - HTML parsing and CSV export
- `requirements.txt` - Python dependencies

## Notes

- Uses persistent browser context to maintain session
- Includes retry logic for reliability
- Respects website structure and includes proper delays
- Browser runs in non-headless mode by default for transparency