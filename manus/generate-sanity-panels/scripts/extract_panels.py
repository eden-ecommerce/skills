import json
import os
import sys


def extract_document_panels(schema_path, doc_name, field_name="panels"):
    if not os.path.exists(schema_path):
        print(f"Error: {schema_path} not found")
        return None

    with open(schema_path, "r") as f:
        schema = json.load(f)

    doc = next(
        (item for item in schema if item.get("name") == doc_name and item.get("type") == "document"),
        None,
    )
    if not doc:
        print(f"Document '{doc_name}' not found")
        return None

    attributes = doc.get("attributes", {})
    panels_attr = attributes.get(field_name, {})
    if not panels_attr:
        print(f"No '{field_name}' attribute on document '{doc_name}'")
        return None

    panel_types = []
    union_of = panels_attr.get("value", {}).get("of", {}).get("of", [])
    for item in union_of:
        inline_name = item.get("rest", {}).get("name")
        if inline_name:
            panel_types.append(inline_name)

    panel_schemas = {}
    for pt in panel_types:
        pt_schema = next(
            (item for item in schema if item.get("name") == pt and item.get("type") == "type"),
            None,
        )
        if pt_schema:
            panel_schemas[pt] = pt_schema

    return panel_schemas


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 extract_panels.py <schema.json> <documentName> [fieldName=panels]")
        sys.exit(1)

    field = sys.argv[3] if len(sys.argv) > 3 else "panels"
    results = extract_document_panels(sys.argv[1], sys.argv[2], field)
    if results:
        print(json.dumps(results, indent=2))
