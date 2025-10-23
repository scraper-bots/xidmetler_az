# Xidmetler.az Web Scraper

A Python web scraper for extracting listings from xidmetler.az, including detailed information and phone numbers via AJAX requests.

## Features

- Scrapes listings from pages 1-50
- Extracts detailed information from each listing page
- Retrieves hidden phone numbers via AJAX API calls
- Saves data in both JSON and CSV formats
- Includes rate limiting to avoid overwhelming the server
- Comprehensive error handling and logging

## Installation

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings (pages 1-50):

```bash
python scraper.py
```

### Custom Usage

You can modify the scraper by editing the `main()` function in `scraper.py`:

```python
# Scrape specific page range (e.g., pages 10-20)
scraper.scrape_pages(start_page=10, end_page=20, delay=1.5)

# Adjust delay between requests (in seconds)
scraper.scrape_pages(start_page=0, end_page=50, delay=2.0)
```

## Output

The scraper generates two output files:

1. **xidmetler_listings.json** - Complete data in JSON format
2. **xidmetler_listings.csv** - Data in CSV format (suitable for Excel)

### Data Fields

Each listing contains:

- `id` - Listing ID
- `listing_code` - Official listing code from the website
- `title` - Listing title
- `url` - Full URL to the listing page
- `price` - Listed price
- `contact_name` - Contact person/company name
- `phone` - Phone number (extracted via AJAX)
- `location` - Location (usually city)
- `date` - Listing date
- `categories` - List of categories
- `description` - Full description text
- `image_url` - Thumbnail image URL
- `images` - List of all image URLs

## Configuration

### Rate Limiting

The scraper includes a delay between requests to avoid overwhelming the server:

- Default delay: 1.5 seconds between requests
- Adjust using the `delay` parameter in `scrape_pages()`

### Page Range

- Default: Pages 0-49 (corresponding to website pages 1-50)
- Modify `start_page` and `end_page` parameters to scrape different ranges

## Technical Details

### Phone Number Extraction

Phone numbers are hidden on the website and require an AJAX POST request to:

```
POST https://xidmetler.az/ajax.php
```

With payload:
- `act=telshow`
- `id={listing_id}`
- `t=product`
- `h={hash_from_page}`
- `rf={referrer_url}`

The scraper automatically extracts the required hash value from each listing page and makes the AJAX call to retrieve the phone number.

### HTML Structure

The scraper targets these HTML elements:

- Listing container: `<div id="prodwrap" class="prodwrap xcol4 clearfix">`
- Individual listings: `<div class="nobj prod">`
- Detail page: `<article>` tag
- Phone trigger: `<div id="telshow">` with data attributes

## Error Handling

The scraper includes comprehensive error handling:

- Logs all errors with timestamps
- Continues scraping if individual listings fail
- Skips pages that fail to load
- Gracefully handles missing data fields

## Logging

The scraper outputs detailed logs showing:

- Pages being fetched
- Number of listings found per page
- Individual listings being scraped
- Any errors encountered
- Total listings scraped

## Notes

- The scraper respects the website by including delays between requests
- Some listings may have missing phone numbers if the AJAX call fails
- Images are saved as URLs, not downloaded locally
- The script maintains a session to preserve cookies across requests

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml

## License

This scraper is for educational purposes only. Please respect the website's terms of service and robots.txt when using this tool.
