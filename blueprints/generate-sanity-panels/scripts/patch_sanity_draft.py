#!/usr/bin/env python3
"""Patch a Sanity draft from draftPatch.json. Project, dataset, token from CLI/env."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cli_env import add_sanity_args, resolve_sanity, sanity_headers, sanity_mutate_url


def mutate(mutations: list, project_id: str, dataset: str, token: str) -> dict:
    url = sanity_mutate_url(project_id, dataset)
    resp = requests.post(
        url, headers=sanity_headers(token), json={"mutations": mutations}, timeout=120
    )
    if resp.status_code >= 400:
        raise SystemExit(f"Mutate failed {resp.status_code}: {resp.text[:500]}")
    return resp.json()


def build_set_fields(patch: dict) -> dict:
    """Merge optional set/fields/top-level extras into one patch set dict."""
    set_fields: dict = {}

    explicit_set = patch.get("set")
    if isinstance(explicit_set, dict):
        set_fields.update(explicit_set)

    extra_fields = patch.get("fields")
    if isinstance(extra_fields, dict):
        set_fields.update(extra_fields)

    panels = patch.get("panels")
    if panels is not None:
        set_fields["panels"] = panels

    for key in ("title", "slug", "groupIds"):
        if key in patch and key not in set_fields:
            set_fields[key] = patch[key]

    return set_fields


def build_mutations(patch: dict) -> list:
    if patch.get("mutations"):
        return patch["mutations"]

    document_id = patch.get("documentId")
    set_fields = build_set_fields(patch)
    if not document_id or not set_fields:
        raise SystemExit(
            "draftPatch must include mutations[] or documentId + panels[] "
            "(optionally set/fields/title)"
        )

    doc_type = patch.get("_type") or patch.get("documentType") or "product"

    return [
        {
            "createIfNotExists": {
                "_id": document_id,
                "_type": doc_type,
            }
        },
        {
            "patch": {
                "id": document_id,
                "set": set_fields,
            }
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch Sanity draft from draftPatch.json")
    parser.add_argument("draft_patch", help="Path to draftPatch.json")
    add_sanity_args(parser)
    args = parser.parse_args()

    project_id, dataset, token = resolve_sanity(args)
    patch = json.loads(Path(args.draft_patch).read_text())
    mutations = build_mutations(patch)
    result = mutate(mutations, project_id, dataset, token)

    document_id = patch.get("documentId")
    panels = patch.get("panels")
    panel_count = len(panels) if panels else None
    if not panel_count and patch.get("mutations"):
        for item in patch["mutations"]:
            panels_in_set = item.get("patch", {}).get("set", {}).get("panels")
            if panels_in_set:
                panel_count = len(panels_in_set)
                break

    out = {
        "ok": True,
        "draftId": document_id,
        "panelCount": panel_count,
        "mutationResult": result,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
