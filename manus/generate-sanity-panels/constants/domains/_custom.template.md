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
| cms.projectId | if Sanity |
| cms.dataset | if Sanity |
| urls.gallery | panel preview base |
| urls.preview | draft preview pattern |
| constraints | hard rules for this site |

Emit same shape as `domainSnapshot` in `definitionBundle`.
