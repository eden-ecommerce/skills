# Publish360

| Field | Value |
|---|---|
| id | `publish360` |
| website | multi-tenant publisher |
| delivery | Publisher CMS + storefront per tenant |
| locale | tenant-defined |
| surfaces | `web-page`, `email` |
| requiresTenantBrief | **true** |

## Tenant brief (required)

Collect before Definition completes:

- tenant name + brand voice
- catalogue source (API, Algolia index, manual list)
- CMS projectId + dataset
- gallery base URL
- preview token policy

Block stage 2 if `tenantBrief` missing.

## Tone

Per tenant brief. Never assume Eden voice.

## CMS

Per tenant. Connector fields from `tenantBrief`.

## Constraints

No cross-tenant defaults. No Eden URLs unless tenant brief says so.
