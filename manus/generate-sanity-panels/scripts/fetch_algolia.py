import os
import requests
import json
import sys

def fetch_product(product_id):
    app_id = os.environ.get('ALGOLIA_APP_ID')
    api_key = os.environ.get('ALGOLIA_SEARCH_KEY')

    if not app_id or not api_key:
        print("Error: Missing ALGOLIA_APP_ID or ALGOLIA_SEARCH_KEY")
        return

    url = f'https://{app_id}-dsn.algolia.net/1/indexes/products/query'
    headers = {
        'X-Algolia-Application-Id': app_id,
        'X-Algolia-API-Key': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'filters': f'product_id:{product_id} AND stores:eden'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching from Algolia: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_algolia.py <product_id>")
        sys.exit(1)
    
    result = fetch_product(sys.argv[1])
    if result:
        print(json.dumps(result, indent=2))
