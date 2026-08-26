#!/usr/bin/env python3
"""Query Eden products index via Algolia. App id + search key from CLI/env — never hardcoded."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cli_env import add_algolia_args, resolve_algolia


def query_algolia(payload: dict, app_id: str, api_key: str) -> dict | None:
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
    parser = argparse.ArgumentParser(description="Query products index via Algolia")
    parser.add_argument("product_id", nargs="?", help="Eden product_id (stores:eden filter)")
    parser.add_argument("--filter", help="Raw Algolia filters string")
    parser.add_argument("--query", help="Algolia query string")
    parser.add_argument("--hits-per-page", type=int, default=20)
    add_algolia_args(parser)
    args = parser.parse_args()

    app_id, api_key = resolve_algolia(args)

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

    result = query_algolia(payload, app_id, api_key)
    if result:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
