# Quick Start Guide

## Running the Full Scraper (Pages 1-50)

To scrape all 50 pages and extract all listings with detailed information:

```bash
python scraper.py
```

This will:
- Scrape pages 0-49 (which correspond to website pages 1-50)
- Extract detailed information from each listing
- Retrieve phone numbers via AJAX calls
- Save results to `xidmetler_listings.json` and `xidmetler_listings.csv`
- Take approximately 1-2 hours to complete (depending on internet speed)

## Testing with a Single Page

To test with a single page first:

```bash
python test_scraper.py
```

This will scrape only page 4 and save results to `test_listings.json` and `test_listings.csv`.

## Customizing the Scraper

Edit `scraper.py` and modify the `main()` function:

```python
def main():
    scraper = XidmetlerScraper()

    # Example: Scrape pages 10-20 only
    scraper.scrape_pages(start_page=10, end_page=20, delay=1.5)

    # Example: Adjust delay between requests (2 seconds)
    scraper.scrape_pages(start_page=0, end_page=50, delay=2.0)

    # Save results
    scraper.save_to_json("my_listings.json")
    scraper.save_to_csv("my_listings.csv")
```

## Output Files

### JSON Format
- File: `xidmetler_listings.json`
- Structure: Array of listing objects
- Best for: Programming, data analysis, APIs

### CSV Format
- File: `xidmetler_listings.csv`
- Structure: Tabular format with headers
- Best for: Excel, Google Sheets, data analysis

## Data Fields Extracted

Each listing contains:
- **id**: Listing ID
- **listing_code**: Official listing code
- **title**: Listing title
- **url**: Full URL to listing page
- **price**: Listed price
- **contact_name**: Contact person/company
- **phone**: Phone number (extracted via AJAX)
- **location**: City/location
- **date**: Listing date
- **categories**: Categories (array)
- **description**: Full description
- **image_url**: Thumbnail image
- **images**: All images (array)

## Important Notes

1. **Rate Limiting**: The scraper includes delays between requests (default 1.5 seconds) to avoid overwhelming the server
2. **Phone Numbers**: Successfully extracted via AJAX API calls
3. **Time Estimate**: Full scrape of 50 pages takes approximately 1-2 hours
4. **Error Handling**: The scraper will continue even if individual listings fail

## Troubleshooting

### No listings found
- Check your internet connection
- Verify the website is accessible
- Run `python debug_scraper.py` to check HTML structure

### Missing phone numbers
- Some listings may not have phone numbers available
- AJAX calls may fail occasionally due to network issues
- Check the logs for specific errors

### Slow scraping
- Adjust the delay parameter (minimum recommended: 1 second)
- Check your internet speed
- Consider scraping in smaller batches

## Example Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Test with 1 page
python test_scraper.py

# Run full scrape (50 pages)
python scraper.py

# View results
head xidmetler_listings.csv
```
