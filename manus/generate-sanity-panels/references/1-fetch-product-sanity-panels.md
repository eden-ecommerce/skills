---
name: fetch-product-sanity-panels
description: HUNT PRODUCT PANELS IN EDEN CMS SCHEMA. USE WHEN NEED KNOW HOW PRODUCT DOCUMENT BUILT. EXTRACT SCHEMAS FOR FEATURED ORGANISATIONS, JOBS, EVENTS, AND BUTTONS.
---

# HUNT PRODUCT PANELS

MANUS WANT PRODUCT SCHEMA? MANUS USE THIS.

## WHY USE?
*   NEED KNOW WHAT PANELS INSIDE PRODUCT.
*   NEED SEE FULL JSON SCHEMA FOR EVERY PANEL TYPE.
*   EDEN CMS CHANGE? THIS FIND TRUTH.

## HOW HUNT (THE STEPS)

### 1. GET BIG JSON MAP
*   MANUS GO URL: `https://cms.eden.co.uk/schema.json`
*   USE `curl` OR `browser`. SAVE TO `schema.json`.

### 2. RUN MAGIC SCRIPT
*   USE SCRIPT IN THIS SKILL: `/home/ubuntu/skills/fetch-product-sanity-panels/scripts/extract_panels.py`
*   COMMAND: `python3 /home/ubuntu/skills/fetch-product-sanity-panels/scripts/extract_panels.py schema.json`

### 3. SEE WHAT FOUND
*   SCRIPT FIND `product` DOCUMENT.
*   SCRIPT FIND `panels` LIST.
*   SCRIPT GRAB FULL SCHEMA FOR ALL PANELS IN UNION.

## CAVE MAN LOGIC (FOR SCRIPT)
*   FIND ITEM WHERE `name` IS "product" AND `type` IS "document".
*   LOOK IN `attributes` FOR `panels`.
*   `panels` IS `union`. FOLLOW `of` -> `of` TO FIND NAMES.
*   FOR EVERY NAME, FIND ITEM WHERE `name` MATCH AND `type` IS "type".
*   GIVE ALL TO USER.

## TROUBLE?
*   IF NO `product`? SCHEMA CHANGE. MANUS MUST `grep` FOR "product" TO FIND NEW PATH.
*   IF NO `panels`? LOOK FOR OTHER ATTRIBUTE NAME.
