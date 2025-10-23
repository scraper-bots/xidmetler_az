#!/usr/bin/env python3
"""
Test script for xidmetler.az scraper
Scrapes only 1 page for testing purposes
"""

from scraper import XidmetlerScraper
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_scraper():
    """Test the scraper with 1 page"""
    logger.info("Starting test scrape...")

    scraper = XidmetlerScraper()

    # Test with just 1 page (page 4 as mentioned by user)
    scraper.scrape_pages(start_page=4, end_page=5, delay=1.5)

    # Save results
    scraper.save_to_json("test_listings.json")
    scraper.save_to_csv("test_listings.csv")

    logger.info(f"Test completed! Scraped {len(scraper.all_listings)} listings")

    # Print first listing as sample
    if scraper.all_listings:
        logger.info("\n" + "="*50)
        logger.info("Sample listing:")
        logger.info("="*50)
        sample = scraper.all_listings[0]
        for key, value in sample.items():
            if key != 'description' and key != 'images':
                logger.info(f"{key}: {value}")
        logger.info("="*50)


if __name__ == "__main__":
    test_scraper()
