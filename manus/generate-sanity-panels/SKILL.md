---
name: generate-sanity-panels
description: Orchestrates the creation and deployment of SEO-optimized product detail page panels in Sanity, following a structured research, prototyping, and verification workflow.
---

# GENERATE SANITY PANELS — MASTER SKILL

## HARD RULES
- ONLY create **draft** documents (`_id` prefixed `drafts.`). NEVER publish without explicit user confirmation.
- ALWAYS prototype in Storybook Sandbox (if available) BEFORE publishing a Sanity draft. Present screenshots to the user for review.
- ALWAYS get user confirmation before deploying a draft to the production Sanity dataset.
- All image assets for panels MUST be uploaded to Sanity to ensure optimization and proper rendering. External URLs are only for prototyping in Storybook where schema allows.
- Secrets (e.g., preview tokens) MUST NOT be exposed in chat history or public files. Use secure channels for sensitive information.

---

## WORKFLOW (10 STEPS)

### STEP 1 — FETCH PRODUCT DATA
1.  **Product ID**: Take a product ID from the user.
2.  **Algolia (`products` index, filter `stores:eden`)**: Fetch comprehensive product data (price, title, author, ISBN, categories, series, related products, images).
3.  **Wide/Deep Research**: Perform comprehensive research on the product and author (image assets, relevant topics/themes, related products, additional information about publisher/author, video assets). Use trusted public sources like official author websites, publisher sites, and reputable review platforms (e.g., Amazon A+ content for inspiration).

### STEP 2 — CONSTRUCT DESIRED PRODUCT PAGE
1.  Based on the research, construct a desired product page layout, organized into logical sections (e.g., Author Spotlight, Key Themes, Related Products, FAQs, Technical Specs).
2.  **Contextual Content**: Ensure all content (text, images, videos) is highly relevant to the product and author. For example:
    *   **Author Spotlight**: Image of the author, bio, links to creator page.
    *   **Publisher Panels**: Based on product information, specs, comparisons.
    *   **Video Panels**: Official YouTube videos from author/publisher.
    *   **C360 & Organisation Panels**: Related assets/resources from internal C360 system or `organisationHub` Algolia index (jobs, events, organizations).
    *   **Hotspots**: Relevant to information on the image, linking to specs or technical details.
    *   **FAQs**: Professional, human tone, short, punchy, informative, no bloat.
    *   **Related Products**: Carousels or grids of related products from Algolia (same author, series, or thematic relevance).

### STEP 3 — FETCH SANITY SCHEMA & PANEL REFERENCES
1.  **Sanity Schema**: Fetch the full production schema from `https://cms.eden.co.uk/schema.json`.
2.  **Panel Visuals**: Access `https://eden-xi.vercel.app/panels/product` (or equivalent reference if this URL changes) to identify rendered HTML, responsiveness, and panel variations. Associate panel titles with Sanity `product.panels` schema types.
3.  **Panel Functionality**: Research the description provided for each panel type in the schema/reference to understand its functionality and intent.

### STEP 4 — PROTOTYPE IN STORYBOOK SANDBOX
1.  **Local Filesystem Check**: Check for the local Storybook sandbox file: `/mnt/desktop/christian-360-next-design/apps/storybook/src/stories/sandbox/Sandbox.stories.tsx`.
2.  **Populate Prototype**: If the file is accessible, update it to render **every panel variation** identified in Step 3, populated with the contextual content from Step 2. Use `PanelBlock` wrappers to label each panel with its `_type`.
3.  **Capture Screenshots**: Capture screenshots of the Storybook prototype and present them to the user for visual review and refinement.
4.  **Fallback**: If local filesystem access is not available, generate ASCII wireframes or detailed textual descriptions of the proposed panel layouts.

### STEP 5 — UPLOAD IMAGES TO SANITY
1.  **Identify Image Needs**: Determine which panels require images and if those images are contextual (e.g., author photo, publisher logo, thematic imagery).
2.  **Upload Process**: Upload all necessary contextual images to Sanity via the Assets API (using `manus-upload-file` to get CDN URLs, then `manus-mcp-cli tool call create_asset` or similar if direct upload is available, or manually if no direct tool is available). This ensures images are optimized and generate valid `sanity.imageAsset.reference` objects.

### STEP 6 — BUILD & PUBLISH SANITY DRAFT
1.  **Fetch Current Document**: Fetch the current product document from production Sanity to get its `_id` and existing `panels` array.
2.  **Construct Payload**: Build the `panels` array with unique `_key` (UUID) for each item, incorporating all contextual content and Sanity asset references for images.
3.  **Deploy Draft**: Use `manus-mcp-cli tool call patch_documents` to update the existing draft document (`_id` prefixed `drafts.`) with the new `panels` array. **User confirmation is required before publishing to production.**

### STEP 7 — VERIFY RENDERED PAGE
1.  **Preview URL**: Use the provided preview URL with the Sanity preview token (e.g., `https://eden-xi.vercel.app/api/preview?type=product&token=<TOKEN>&slug=<ID>`) to view the rendered draft page.
2.  **Visual Check**: Verify that the actual page matches the Storybook prototype (or ASCII wireframes) and that all panels render correctly with their contextual content and images.
3.  **Fixes**: Apply any necessary fixes to the Sanity draft based on the verification.

### STEP 8 — USER PERMISSION TO PUBLISH
1.  **Request Approval**: Ask the user for explicit permission to publish the draft document to production.

### STEP 9 — PUBLISH TO PRODUCTION
1.  **Publish**: Upon user approval, use `manus-mcp-cli tool call publish_documents` to publish the draft to production.

### STEP 10 — CREATE REVIEW DOCUMENT
1.  **Review Document**: Create a comprehensive review document with findings, analysis, and a score for the produced page, including constructive feedback for further improvements.

---

## MEMORY BANK
- **Component map**: `/home/ubuntu/memory/panels/component_map.json` (mapping Sanity panel types to their visual representation/functionality)
- **Panel context map**: `/home/ubuntu/memory/panel_context_map.json` (detailed rules for populating each panel type)
- **Product research**: `/home/ubuntu/memory/<product_id>_research.json` (all deep research findings for a product)
- **Uploaded assets**: `/home/ubuntu/memory/uploaded_assets.json` (map of uploaded image CDN URLs and Sanity asset IDs)

---

## TOKEN USAGE OPTIMIZATION
- Maximize use of the memory bank to store fetched schemas, research data, and asset IDs, avoiding redundant network calls and context re-reads.
- Keep `SKILL.md` concise, focusing on rules and workflow steps.
- Only load specific skill references or schema parts relevant to the current step.

---

## SECRETS MANAGEMENT
- Sanity API tokens are managed securely by the MCP connector. Do NOT attempt to extract or display them.
- Preview tokens are provided by the user and should be treated as sensitive. Do NOT log or store them in public files.
