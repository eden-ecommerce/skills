#!/usr/bin/env python3
"""Upload a local image to Sanity assets. Project, dataset, token from CLI/env."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cli_env import add_sanity_args, resolve_sanity, sanity_assets_url


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload an image file to Sanity")
    parser.add_argument("image_path", help="Local image file")
    parser.add_argument("--filename", help="Asset filename (defaults to local name)")
    add_sanity_args(parser)
    args = parser.parse_args()

    project_id, dataset, token = resolve_sanity(args)
    path = Path(args.image_path)
    if not path.is_file():
        raise SystemExit(f"File not found: {path}")

    filename = args.filename or path.name
    url = sanity_assets_url(project_id, dataset, quote(filename))
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, headers=headers, data=path.read_bytes(), timeout=120)
    if resp.status_code >= 400:
        raise SystemExit(f"Upload failed {resp.status_code}: {resp.text[:500]}")
    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    main()
