---
name: fetch-product-document-from-sanity
description: HUNT PRODUCT DOCUMENT IN SANITY. USE WHEN NEED SEE CMS PANELS, CONFIG, AND GROQ DATA. TARGETS EDEN PROJECT AND DATASET.
---

# HUNT SANITY PRODUCT

MANUS WANT CMS DOCUMENT? MANUS USE THIS.

## WHY USE?
*   NEED SEE WHAT PANELS ON PAGE.
*   NEED SEE CMS CONFIG FOR PRODUCT.
*   NEED FETCH DATA WITH GROQ.

## HOW HUNT (THE STEPS)

### 1. USE MCP TOOL
*   MANUS USE `manus-mcp-cli` TOOL.
*   SERVER IS `sanity`.
*   PROJECT ID IS `bct7esy7`.
*   DATASET IS `eden`.

### 2. RUN GROQ QUERY
*   COMMAND:
```bash
manus-mcp-cli tool call query_documents --server sanity --input '{
  "query": "*[_type == \"product\" && product_id == \"<PRODUCT_ID>\"][0]",
  "resource": {
    "projectId": \"bct7esy7\",
    "dataset": \"eden\"
  }
}'
```

### 3. SEE WHAT FOUND
*   SANITY GIVE BACK BIG JSON.
*   JSON HAS `panels` LIST.
*   JSON HAS `_id` AND `_type`.

## CAVE MAN LOGIC
*   TALK TO SANITY SERVER THROUGH MCP.
*   GIVE PROJECT AND DATASET NAME.
*   ASK FOR DOCUMENT WITH MATCHING PRODUCT ID.
*   SHOW PANELS TO MANUS.

## TROUBLE?
*   EMPTY RESULT? CHECK IF PRODUCT ID IS STRING OR NUMBER IN CMS.
*   DATASET NOT FOUND? CHECK IF `eden` OR `production` NEEDED.
