# Epstein Files API

A free, public REST API to programmatically access the Epstein investigation archive hosted at [exposingepstein.com](https://exposingepstein.com).

The archive contains thousands of videos, court documents, and PDFs from the Epstein case — all tagged, searchable, and now accessible to researchers, journalists, and developers.

---

## Base URL

```
https://exposingepstein.com/backend/api/api_public.php
```

## Authentication

All endpoints (except `register`) require an API key.

Get your free key in seconds:

```bash
curl -s -X POST "https://exposingepstein.com/backend/api/api_public.php?action=register" \
  -H "Content-Type: application/json" \
  -d '{"app_name": "my-app", "email": "you@example.com"}'
```

Pass your key on every request via header (recommended) or query param:

```
X-Api-Key: your_api_key_here
```
or
```
?api_key=your_api_key_here
```

**Rate limit:** 500 requests / day. No cost, no credit card.

---

## Endpoints

### List Documents

```
GET ?action=documents
```

Returns a paginated list of videos and PDFs from the archive.

**Parameters**

| Name    | Type   | Default | Description                              |
|---------|--------|---------|------------------------------------------|
| `type`  | string | `all`   | Filter by type: `all`, `video`, `pdf`    |
| `page`  | int    | `1`     | Page number                              |
| `limit` | int    | `20`    | Results per page (max 50)                |
| `tag`   | string | —       | Filter by tag name (case-insensitive)    |
| `efta`  | string | —       | Filter by source/provenance identifier   |

**Example**

```bash
curl "https://exposingepstein.com/backend/api/api_public.php?action=documents&type=video&limit=5&page=1" \
  -H "X-Api-Key: your_api_key_here"
```

**Response**

```json
{
  "success": true,
  "version": "v1",
  "data": [
    {
      "id": 1,
      "type": "video",
      "efta": "EFTA-0001",
      "description": "Deposition footage – Palm Beach, 2005",
      "tags": ["deposition", "palm-beach", "2005"]
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 5,
    "total": 983,
    "has_more": true
  }
}
```

---

### Get a Single Document

```
GET ?action=document&id=<id>&type=<video|pdf>
```

**Parameters**

| Name   | Type   | Required | Description                    |
|--------|--------|----------|--------------------------------|
| `id`   | int    | yes      | Document sequence ID           |
| `type` | string | yes      | `video` or `pdf`               |

**Example**

```bash
curl "https://exposingepstein.com/backend/api/api_public.php?action=document&id=42&type=video" \
  -H "X-Api-Key: your_api_key_here"
```

**Response**

```json
{
  "success": true,
  "version": "v1",
  "data": {
    "id": 42,
    "type": "video",
    "efta": "EFTA-0042",
    "description": "Surveillance footage – Little Saint James",
    "created_at": "2024-03-15T10:22:00",
    "tags": ["surveillance", "island", "little-saint-james"]
  }
}
```

---

### Search

```
GET ?action=search&q=<query>
```

Full-text search across document descriptions, tags, and source identifiers.

**Parameters**

| Name    | Type   | Default | Description                              |
|---------|--------|---------|------------------------------------------|
| `q`     | string | —       | Search query (min 2 characters, required)|
| `type`  | string | `all`   | Filter by type: `all`, `video`, `pdf`    |
| `page`  | int    | `1`     | Page number                              |
| `limit` | int    | `20`    | Results per page (max 50)                |

**Example**

```bash
curl "https://exposingepstein.com/backend/api/api_public.php?action=search&q=maxwell&type=pdf" \
  -H "X-Api-Key: your_api_key_here"
```

**Response**

```json
{
  "success": true,
  "version": "v1",
  "query": "maxwell",
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 134,
    "has_more": true
  }
}
```

---

### List Tags

```
GET ?action=tags
```

Returns all approved tags with their document counts, sorted by popularity.

**Parameters**

| Name   | Type   | Default | Description                           |
|--------|--------|---------|---------------------------------------|
| `type` | string | `all`   | `all`, `video`, or `pdf`              |

**Example**

```bash
curl "https://exposingepstein.com/backend/api/api_public.php?action=tags&type=all" \
  -H "X-Api-Key: your_api_key_here"
```

**Response**

```json
{
  "success": true,
  "version": "v1",
  "data": [
    { "name": "maxwell",       "count": 312 },
    { "name": "palm-beach",    "count": 287 },
    { "name": "little-saint-james", "count": 241 },
    { "name": "deposition",   "count": 198 }
  ],
  "total": 1847
}
```

---

### Platform Stats

```
GET ?action=stats
```

Returns aggregate counts for the archive.

**Example**

```bash
curl "https://exposingepstein.com/backend/api/api_public.php?action=stats" \
  -H "X-Api-Key: your_api_key_here"
```

**Response**

```json
{
  "success": true,
  "version": "v1",
  "data": {
    "videos": 983,
    "pdfs": 4821,
    "tags": 1847,
    "total": 5804,
    "last_updated": "2026-04-16"
  }
}
```

---

## Register for an API Key

```
POST ?action=register
```

**Body (JSON)**

| Field         | Type   | Required | Description                          |
|---------------|--------|----------|--------------------------------------|
| `app_name`    | string | yes      | Name of your application             |
| `email`       | string | yes      | Your contact email                   |
| `origin_url`  | string | no       | Your website or app URL              |
| `description` | string | no       | Brief description of how you use it  |

**Example**

```bash
curl -X POST "https://exposingepstein.com/backend/api/api_public.php?action=register" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name":    "epstein-research-tool",
    "email":       "researcher@example.com",
    "origin_url":  "https://myresearchtool.com",
    "description": "Building a public timeline of the Epstein case"
  }'
```

**Response**

```json
{
  "success": true,
  "message": "API key issued. Include it in every request as X-Api-Key header.",
  "api_key": "a3f8c2e1d9b047...",
  "rate_limit": "500 requests/day",
  "docs": "https://github.com/G103L3/epstein-files-api"
}
```

---

## Error Responses

All errors return `"success": false` with a machine-readable `code` field.

| HTTP Status | Code            | Meaning                                         |
|-------------|-----------------|--------------------------------------------------|
| 400         | `BAD_REQUEST`   | Missing or invalid parameters                   |
| 401         | `NO_API_KEY`    | API key not provided                            |
| 401         | `INVALID_KEY`   | API key does not exist                          |
| 403         | `KEY_DISABLED`  | API key has been disabled                       |
| 404         | `NOT_FOUND`     | Document not found                              |
| 429         | `RATE_LIMIT`    | Daily limit reached (resets after 24 h)         |

**Example error response**

```json
{
  "success": false,
  "error": "Invalid API key.",
  "code": "INVALID_KEY"
}
```

---

## Code Examples

### Python

```python
import requests

API_KEY  = "your_api_key_here"
BASE_URL = "https://exposingepstein.com/backend/api/api_public.php"
HEADERS  = {"X-Api-Key": API_KEY}

# Search for documents mentioning Maxwell
resp = requests.get(BASE_URL, params={"action": "search", "q": "maxwell", "type": "pdf"}, headers=HEADERS)
data = resp.json()

for doc in data["data"]:
    print(f"[{doc['type'].upper()}] id={doc['id']}  tags={doc['tags']}")
```

### JavaScript / Node.js

```js
const BASE = "https://exposingepstein.com/backend/api/api_public.php";
const KEY  = "your_api_key_here";

async function search(query, type = "all") {
  const url = `${BASE}?action=search&q=${encodeURIComponent(query)}&type=${type}`;
  const res  = await fetch(url, { headers: { "X-Api-Key": KEY } });
  return res.json();
}

const results = await search("palm beach");
console.log(`Found ${results.pagination.total} documents`);
results.data.forEach(d => console.log(`${d.type} #${d.id} — ${d.description}`));
```

### curl (one-liner search)

```bash
curl -s "https://exposingepstein.com/backend/api/api_public.php?action=search&q=deposition" \
  -H "X-Api-Key: your_key" | python3 -m json.tool
```

---

## What the API Does NOT Expose

- User accounts, emails, or any personal data
- Internal database IDs or authentication tokens
- Comments, votes, or community activity
- Admin-only content or unpublished documents
- Raw file URLs (to prevent direct hotlinking; visit [exposingepstein.com](https://exposingepstein.com) to view files)

---

## Terms of Use

- This API is provided free of charge for research, journalism, and public interest projects.
- Do not use it to build products that misrepresent, manipulate, or profit from the victims of Jeffrey Epstein.
- We reserve the right to revoke keys used in violation of these terms.
- The archive is maintained by volunteers. Please be respectful of the rate limits.

---

## About the Archive

[ExposingEpstein.com](https://exposingepstein.com) is an independent investigation platform. The archive includes court documents, deposition videos, surveillance footage, and other materials related to the Jeffrey Epstein case and associated individuals — assembled to support accountability and public understanding.

---

## Contributing

Found a bug or want a new endpoint? Open an [issue](https://github.com/G103L3/epstein-files-api/issues) or submit a pull request.
