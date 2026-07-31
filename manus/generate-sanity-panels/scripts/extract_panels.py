import json
import sys
import os

def extract_product_panels(schema_path):
    if not os.path.exists(schema_path):
        print(f"Error: {schema_path} not found")
        return

    with open(schema_path, 'r') as f:
        schema = json.load(f)

    # Find the product document
    product_doc = next((item for item in schema if item.get('name') == 'product' and item.get('type') == 'document'), None)

    if not product_doc:
        print("Product document not found")
        return

    # Get the panels attribute
    attributes = product_doc.get('attributes', {})
    panels_attr = attributes.get('panels', {})

    if not panels_attr:
        print("No panels attribute found in product document")
        return

    # Extract the names of the panel types
    panel_types = []
    # Structure: panels -> value -> of -> of -> [items]
    union_of = panels_attr.get('value', {}).get('of', {}).get('of', [])
    for item in union_of:
        inline_name = item.get('rest', {}).get('name')
        if inline_name:
            panel_types.append(inline_name)

    # Fetch the full schema for each panel type
    panel_schemas = {}
    for pt in panel_types:
        pt_schema = next((item for item in schema if item.get('name') == pt and item.get('type') == 'type'), None)
        if pt_schema:
            panel_schemas[pt] = pt_schema

    return panel_schemas

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_panels.py <path_to_schema.json>")
        sys.exit(1)
    
    results = extract_product_panels(sys.argv[1])
    if results:
        print(json.dumps(results, indent=2))
