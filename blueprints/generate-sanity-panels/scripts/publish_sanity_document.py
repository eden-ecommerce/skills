#!/usr/bin/env python3
"""Publish a Sanity document via the actions API. Project, dataset, token from CLI/env."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cli_env import add_sanity_args, resolve_sanity, sanity_actions_url, sanity_headers


def publish_ids(document_id: str) -> tuple[str, str]:
    if document_id.startswith("drafts."):
        return document_id, document_id.removeprefix("drafts.")
    return f"drafts.{document_id}", document_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a Sanity document")
    parser.add_argument("document_id", help="Draft or published document id")
    add_sanity_args(parser)
    args = parser.parse_args()

    project_id, dataset, token = resolve_sanity(args)
    draft_id, published_id = publish_ids(args.document_id)

    payload = {
        "actions": [
            {
                "actionType": "sanity.action.document.publish",
                "draftId": draft_id,
                "publishedId": published_id,
            }
        ]
    }
    url = sanity_actions_url(project_id, dataset)
    resp = requests.post(url, headers=sanity_headers(token), json=payload, timeout=60)
    if resp.status_code >= 400:
        raise SystemExit(f"Publish failed {resp.status_code}: {resp.text[:500]}")

    out = {"ok": True, "publishedId": published_id, "result": resp.json()}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
