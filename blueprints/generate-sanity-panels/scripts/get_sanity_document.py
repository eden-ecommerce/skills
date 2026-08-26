#!/usr/bin/env python3
"""GROQ query against Sanity HTTP API. Project, dataset, token from CLI/env."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cli_env import add_sanity_args, resolve_sanity, sanity_headers, sanity_query_url


def main() -> None:
    parser = argparse.ArgumentParser(description="Query Sanity via GROQ")
    parser.add_argument("--query", help="GROQ query string")
    parser.add_argument("--product-id", help="Shorthand: product doc by product_id")
    parser.add_argument("--slug", help="Shorthand: article doc by slug.current")
    add_sanity_args(parser)
    args = parser.parse_args()

    project_id, dataset, token = resolve_sanity(args)

    query = args.query
    if args.product_id:
        query = f'*[_type == "product" && product_id == "{args.product_id}"][0]'
    elif args.slug:
        query = f'*[_type == "article" && slug.current == "{args.slug}"][0]'
    if not query:
        raise SystemExit("Provide --query, --product-id, or --slug")

    url = sanity_query_url(project_id, dataset)
    resp = requests.get(url, headers=sanity_headers(token), params={"query": query}, timeout=60)
    if resp.status_code >= 400:
        raise SystemExit(f"Query failed {resp.status_code}: {resp.text[:500]}")
    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    main()
