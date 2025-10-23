#!/usr/bin/env python3
"""
Custom scraper with command-line arguments
Usage: python scrape_custom.py --start 0 --end 10 --delay 1.5
"""

import argparse
from scraper import XidmetlerScraper
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Scrape listings from xidmetler.az',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape pages 0-9 (first 10 pages)
  python scrape_custom.py --start 0 --end 10

  # Scrape pages 20-30 with 2 second delay
  python scrape_custom.py --start 20 --end 30 --delay 2.0

  # Scrape all 50 pages with custom output files
  python scrape_custom.py --start 0 --end 50 --json my_data.json --csv my_data.csv
        """
    )

    parser.add_argument(
        '--start',
        type=int,
        default=0,
        help='Starting page number (default: 0)'
    )

    parser.add_argument(
        '--end',
        type=int,
        default=50,
        help='Ending page number (default: 50)'
    )

    parser.add_argument(
        '--delay',
        type=float,
        default=1.5,
        help='Delay between requests in seconds (default: 1.5)'
    )

    parser.add_argument(
        '--json',
        type=str,
        default='xidmetler_listings.json',
        help='Output JSON filename (default: xidmetler_listings.json)'
    )

    parser.add_argument(
        '--csv',
        type=str,
        default='xidmetler_listings.csv',
        help='Output CSV filename (default: xidmetler_listings.csv)'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.start < 0:
        parser.error("Start page must be >= 0")
    if args.end <= args.start:
        parser.error("End page must be > start page")
    if args.delay < 0.5:
        parser.error("Delay must be >= 0.5 seconds")

    logger.info(f"Starting scraper with parameters:")
    logger.info(f"  Pages: {args.start} to {args.end-1}")
    logger.info(f"  Delay: {args.delay} seconds")
    logger.info(f"  JSON output: {args.json}")
    logger.info(f"  CSV output: {args.csv}")

    # Create scraper and run
    scraper = XidmetlerScraper()
    scraper.scrape_pages(
        start_page=args.start,
        end_page=args.end,
        delay=args.delay
    )

    # Save results
    scraper.save_to_json(args.json)
    scraper.save_to_csv(args.csv)

    logger.info(f"\nScraping completed!")
    logger.info(f"Total listings scraped: {len(scraper.all_listings)}")
    logger.info(f"JSON saved to: {args.json}")
    logger.info(f"CSV saved to: {args.csv}")


if __name__ == "__main__":
    main()
