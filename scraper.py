#!/usr/bin/env python3
"""
Xidmetler.az Web Scraper
Scrapes listings from pages 1-50 and extracts detailed information including phone numbers
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XidmetlerScraper:
    """Scraper for xidmetler.az website"""

    BASE_URL = "https://xidmetler.az"
    LISTING_URL = f"{BASE_URL}/homelist/"
    AJAX_URL = f"{BASE_URL}/ajax.php"

    def __init__(self):
        """Initialize the scraper with session and headers"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
        })
        self.all_listings = []

    def get_listing_page(self, page_num: int) -> Optional[BeautifulSoup]:
        """
        Fetch a listing page by page number

        Args:
            page_num: Page number to fetch (0-indexed for start parameter)

        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            url = f"{self.LISTING_URL}?start={page_num}"
            logger.info(f"Fetching listing page: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching page {page_num}: {e}")
            return None

    def extract_listings_from_page(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract all listings from a page

        Args:
            soup: BeautifulSoup object of the page

        Returns:
            List of dictionaries containing listing basic info
        """
        listings = []
        prodwrap = soup.find('div', {'id': 'prodwrap'})

        if not prodwrap:
            logger.warning("No prodwrap found on page")
            return listings

        # Find all listing divs that have both 'nobj' and 'prod' classes
        listing_divs = prodwrap.find_all('div', class_=lambda x: x and 'nobj' in x and 'prod' in x)
        logger.info(f"Found {len(listing_divs)} listings on page")

        for div in listing_divs:
            try:
                # Extract link
                link_tag = div.find('a', href=True)
                if not link_tag:
                    continue

                listing_url = urljoin(self.BASE_URL, link_tag['href'])

                # Extract listing ID from URL
                listing_id_match = re.search(r'-(\d+)\.html', listing_url)
                listing_id = listing_id_match.group(1) if listing_id_match else None

                # Extract title
                title_tag = div.find('div', {'class': 'prodname'})
                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                # Extract image
                img_tag = div.find('img')
                image_url = urljoin(self.BASE_URL, img_tag['src']) if img_tag and img_tag.get('src') else None

                # Extract price
                price_tag = div.find('span', {'class': 'sprice'})
                price = price_tag.get_text(strip=True) if price_tag else "N/A"

                listing = {
                    'id': listing_id,
                    'title': title,
                    'url': listing_url,
                    'image_url': image_url,
                    'price': price
                }
                listings.append(listing)

            except Exception as e:
                logger.error(f"Error extracting listing: {e}")
                continue

        return listings

    def get_phone_number(self, listing_id: str, hash_value: str, referrer: str) -> Optional[str]:
        """
        Get phone number via AJAX request

        Args:
            listing_id: ID of the listing
            hash_value: Hash value from the page
            referrer: Referrer URL

        Returns:
            Phone number string or None
        """
        try:
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': self.BASE_URL,
                'Referer': referrer
            }

            payload = {
                'act': 'telshow',
                'id': listing_id,
                't': 'product',
                'h': hash_value,
                'rf': referrer.replace(self.BASE_URL + '/', '')
            }

            response = self.session.post(
                self.AJAX_URL,
                data=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            if data.get('ok') == 1:
                return data.get('tel')

        except Exception as e:
            logger.error(f"Error fetching phone number for listing {listing_id}: {e}")

        return None

    def extract_detail_info(self, listing_url: str, listing_id: str) -> Dict:
        """
        Extract detailed information from a listing page

        Args:
            listing_url: URL of the listing detail page
            listing_id: ID of the listing

        Returns:
            Dictionary containing detailed listing information
        """
        detail_info = {}

        try:
            logger.info(f"Fetching detail page: {listing_url}")
            response = self.session.get(listing_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            h1_tag = soup.find('h1')
            detail_info['title'] = h1_tag.get_text(strip=True) if h1_tag else "N/A"

            # Extract listing code
            code_tag = soup.find('span', {'class': 'open_idshow'})
            if code_tag:
                code_text = code_tag.get_text(strip=True)
                code_match = re.search(r'(\d+)', code_text)
                detail_info['listing_code'] = code_match.group(1) if code_match else listing_id
            else:
                detail_info['listing_code'] = listing_id

            # Extract category
            article = soup.find('article')
            if article:
                category_links = article.find_all('a', href=True)
                categories = [a.get_text(strip=True) for a in category_links[:2] if '/usta-xidmeti' in a['href'] or '/cam-balkon' in a['href']]
                detail_info['categories'] = categories if categories else ["N/A"]
            else:
                detail_info['categories'] = ["N/A"]

            # Extract price
            price_tag = soup.find('span', {'class': 'pricecolor'})
            detail_info['price'] = price_tag.get_text(strip=True) if price_tag else "N/A"

            # Extract description
            desc_tag = soup.find('p', {'class': 'infop100 fullteshow'})
            detail_info['description'] = desc_tag.get_text(strip=True) if desc_tag else "N/A"

            # Extract contact info
            contact_div = soup.find('div', {'class': 'infocontact'})
            if contact_div:
                # Contact name
                user_span = contact_div.find('span', {'class': 'glyphicon-user'})
                if user_span and user_span.next_sibling:
                    detail_info['contact_name'] = user_span.next_sibling.strip()
                else:
                    detail_info['contact_name'] = "N/A"

                # Location
                location_span = contact_div.find('span', {'class': 'glyphicon-map-marker'})
                if location_span and location_span.next_sibling:
                    detail_info['location'] = location_span.next_sibling.strip()
                else:
                    detail_info['location'] = "N/A"
            else:
                detail_info['contact_name'] = "N/A"
                detail_info['location'] = "N/A"

            # Extract phone number (requires AJAX call)
            # Find the telshow div to get hash
            telshow_div = soup.find('div', {'id': 'telshow'})
            if telshow_div:
                hash_value = telshow_div.get('data-h')
                referrer_value = telshow_div.get('data-rf', '')

                if hash_value:
                    phone = self.get_phone_number(listing_id, hash_value, listing_url)
                    detail_info['phone'] = phone if phone else "N/A"
                else:
                    detail_info['phone'] = "N/A"
            else:
                detail_info['phone'] = "N/A"

            # Extract date
            date_span = soup.find('span', {'class': 'viewsbb'})
            if date_span:
                date_text = date_span.get_text(strip=True)
                date_match = re.search(r'Tarix:\s*(.+)', date_text)
                detail_info['date'] = date_match.group(1) if date_match else "N/A"
            else:
                detail_info['date'] = "N/A"

            # Extract images
            pics_div = soup.find('div', {'id': 'picsopen'})
            images = []
            if pics_div:
                img_links = pics_div.find_all('a', {'rel': 'slider'})
                for link in img_links:
                    img_url = link.get('href')
                    if img_url:
                        images.append(urljoin(self.BASE_URL, img_url))
            detail_info['images'] = images

        except Exception as e:
            logger.error(f"Error extracting detail info from {listing_url}: {e}")

        return detail_info

    def scrape_pages(self, start_page: int = 0, end_page: int = 50, delay: float = 1.0):
        """
        Scrape multiple pages of listings

        Args:
            start_page: Starting page number (0-indexed)
            end_page: Ending page number (exclusive)
            delay: Delay between requests in seconds
        """
        logger.info(f"Starting scrape from page {start_page} to {end_page-1}")

        for page_num in range(start_page, end_page):
            # Fetch listing page
            soup = self.get_listing_page(page_num)
            if not soup:
                logger.warning(f"Skipping page {page_num} due to fetch error")
                continue

            # Extract listings
            listings = self.extract_listings_from_page(soup)

            # For each listing, get detailed info
            for listing in listings:
                if listing['id'] and listing['url']:
                    # Add delay between detail page requests
                    time.sleep(delay)

                    # Get detailed info
                    detail_info = self.extract_detail_info(listing['url'], listing['id'])

                    # Merge basic and detail info
                    full_listing = {**listing, **detail_info}
                    self.all_listings.append(full_listing)

                    logger.info(f"Scraped listing {listing['id']}: {listing['title']}")

            logger.info(f"Completed page {page_num}, total listings: {len(self.all_listings)}")

            # Add delay between page requests
            time.sleep(delay)

    def save_to_json(self, filename: str = "xidmetler_listings.json"):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.all_listings, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.all_listings)} listings to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")

    def save_to_csv(self, filename: str = "xidmetler_listings.csv"):
        """Save scraped data to CSV file"""
        if not self.all_listings:
            logger.warning("No listings to save")
            return

        try:
            # Define CSV fields
            fieldnames = [
                'id', 'listing_code', 'title', 'url', 'price',
                'contact_name', 'phone', 'location', 'date',
                'categories', 'description', 'image_url', 'images'
            ]

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()

                for listing in self.all_listings:
                    # Convert lists to strings for CSV
                    row = listing.copy()
                    if 'categories' in row and isinstance(row['categories'], list):
                        row['categories'] = ', '.join(row['categories'])
                    if 'images' in row and isinstance(row['images'], list):
                        row['images'] = ', '.join(row['images'])
                    writer.writerow(row)

            logger.info(f"Saved {len(self.all_listings)} listings to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")


def main():
    """Main execution function"""
    scraper = XidmetlerScraper()

    # Scrape pages 0-49 (which corresponds to pages 1-50)
    # Note: The URL parameter ?start=0 is page 1, ?start=1 is page 2, etc.
    scraper.scrape_pages(start_page=0, end_page=50, delay=1.5)

    # Save results
    scraper.save_to_json()
    scraper.save_to_csv()

    logger.info(f"Scraping completed! Total listings scraped: {len(scraper.all_listings)}")


if __name__ == "__main__":
    main()
