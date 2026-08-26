# Custom domain template

Copy to new file or fill inline at Definition. User must supply all fields.

| Field | User supplies |
|---|---|
| id | short slug |
| website | public site name or URL |
| delivery | one-line what this site is |
| locale | e.g. UK English |
| surfaces | `web-page` \| `email` \| `app-surface` |
| requiresTenantBrief | true if multi-tenant |
| tone | voice rules |
| catalogue | where products/content live |
| cms.provider | Sanity or other |
| cms.projectId | if Sanity — user supplies at FIRST RUN |
| cms.dataset | if Sanity — user supplies at FIRST RUN |
| cms.schemaUrl | if Sanity — public schema JSON URL |
| urls.gallery | panel preview base (user-supplied host) |
| urls.preview | draft preview pattern (token substituted at Stage 7 from session)
| constraints | hard rules for this site |

Emit same shape as `domainSnapshot` in `definitionBundle`.
