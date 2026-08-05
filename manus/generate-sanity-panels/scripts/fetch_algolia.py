import argparse
import json
import os
import sys

import requests


def query_algolia(payload: dict) -> dict | None:
    app_id = os.environ.get("ALGOLIA_APP_ID")
    api_key = os.environ.get("ALGOLIA_SEARCH_KEY")
    if not app_id or not api_key:
        print("Error: Missing ALGOLIA_APP_ID or ALGOLIA_SEARCH_KEY")
        return None

    url = f"https://{app_id}-dsn.algolia.net/1/indexes/products/query"
    headers = {
        "X-Algolia-Application-Id": app_id,
        "X-Algolia-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        print(f"Error fetching from Algolia: {exc}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Query Eden products index via Algolia")
    parser.add_argument("product_id", nargs="?", help="Eden product_id (stores:eden filter)")
    parser.add_argument("--filter", help="Raw Algolia filters string")
    parser.add_argument("--query", help="Algolia query string")
    parser.add_argument("--hits-per-page", type=int, default=20)
    args = parser.parse_args()

    if args.filter:
        filters = args.filter
    elif args.product_id:
        filters = f"product_id:{args.product_id} AND stores:eden"
    else:
        print("Usage: fetch_algolia.py <product_id> | --filter <filters> [--query <q>]")
        sys.exit(1)

    payload: dict = {"filters": filters, "hitsPerPage": args.hits_per_page}
    if args.query:
        payload["query"] = args.query

    result = query_algolia(payload)
    if result:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
