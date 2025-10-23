#!/usr/bin/env python3
"""
Debug script to check HTML structure
"""

import requests
from bs4 import BeautifulSoup

def debug_page(page_num=0):
    """Debug a single page"""
    url = f"https://xidmetler.az/homelist/?start={page_num}"
    print(f"Fetching: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Check for prodwrap
    prodwrap = soup.find('div', {'id': 'prodwrap'})
    print(f"Found prodwrap: {prodwrap is not None}")

    if prodwrap:
        # Try different class combinations
        listings1 = prodwrap.find_all('div', class_='nobj prod')
        listings2 = prodwrap.find_all('div', class_='nobj')
        listings3 = prodwrap.find_all('div', {'class': lambda x: x and 'nobj' in x})

        print(f"Listings with 'nobj prod': {len(listings1)}")
        print(f"Listings with 'nobj': {len(listings2)}")
        print(f"Listings with 'nobj' in class: {len(listings3)}")

        # Print first div class to see actual structure
        first_div = prodwrap.find('div')
        if first_div:
            print(f"First div classes: {first_div.get('class')}")
            print(f"First div HTML (first 200 chars): {str(first_div)[:200]}")
    else:
        # Print part of the HTML to see structure
        print("\nHTML snippet (first 2000 chars):")
        print(response.text[:2000])

if __name__ == "__main__":
    print("="*50)
    print("Testing page 0:")
    print("="*50)
    debug_page(0)
    print("\n" + "="*50)
    print("Testing page 4:")
    print("="*50)
    debug_page(4)
