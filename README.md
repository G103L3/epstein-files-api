# Epstein Files API

A free, public REST API to programmatically access the Epstein investigation archive at [exposingepstein.com](https://exposingepstein.com).

---

## The Story Behind This

When the U.S. Department of Justice released the Epstein files, they dumped everything into a barely searchable, poorly organized pile. Hundreds of thousands of documents, emails, flight records, photos, and videos with no real way to navigate them. Most people looked at it, felt overwhelmed, and moved on.

We did not.

This project started as something small. Me and [AquaBomber](https://www.reddit.com/user/AquaBomber) just wanted to build something that actually worked. A real archive. Something you could search, browse, and make sense of. What followed was one of the longest and most intense periods of my life.

The way we worked was simple. AquaBomber was out there every day talking to people. He read every comment, every complaint, every request. He understood what the community actually needed and brought it back to me in plain terms. He was the bridge between thousands of strangers on the internet and the code I was writing alone at my desk. Without him keeping that channel open, this project would have died quietly after the first version.

I coded. Every day. From morning until late into the night, sometimes past 3am. Feature after feature, bug after bug, rebuild after rebuild. The stack grew, the database grew, the complexity grew. I did not stop.

Then one day the traffic spiked. Not gradually. In the space of four minutes we went up **6700%**. The server started buckling. I had eight minutes to migrate everything before it went down completely. I did it in eight minutes. Not because I had a plan ready. Because at that point I knew that codebase like I knew my own hands.

What followed was a stretch of sleepless nights I do not fully remember. Monitoring dashboards at 2am. Waking up to check if the site was still up. Pushing fixes while half asleep. The kind of sustained pressure that either breaks a project or hardens it into something real. This one got harder.

The community responded in a way neither of us expected. The [first major update post](https://www.reddit.com/r/Epstein/comments/1rkzcpe/) got hundreds of upvotes. People started depending on the platform. Then came the [full platform launch](https://www.reddit.com/r/Epstein/comments/1sfyd7v/), 5,500 upvotes and 173 comments, researchers and journalists and people who had been following this case for years finally saying they had a tool that matched their level of seriousness.

Today the platform holds:

- Over **180,000 photos** from the DOJ seizure
- Over **2,000 videos**, many with transcriptions and audio analysis
- Thousands of **court documents, emails, and flight records**, tagged and cross-referenced
- A **full-text search** that works across hundreds of thousands of PDFs
- **User accounts**, community posts, comments, voting, and collaborative investigations
- A complete **UI redesign** built directly from community feedback

None of this had a budget. No company, no team, no investors. Just two people who refused to let the files disappear into irrelevance, and a community that kept showing up.

This API is the next step. If you are a researcher, a developer, or a journalist, you should not have to scrape or reverse-engineer anything to access this data. It should be available, clean, and documented.

So here it is.

---

## Base URL

```
https://exposingepstein.com/backend/api/api_public.php
```

## Getting an API Key

API keys are tied to verified developer accounts. The process is straightforward:

1. **Create a free account** at [exposingepstein.com](https://exposingepstein.com) — no email required for a standard account.
2. **Go to Profile → Settings → Developer Account** and click **Apply for Developer Account**.
3. Fill in the required details: contact email, name, and address. These are used only for account verification and are never shared publicly.
4. **Verify your email** — a confirmation link will be sent to the address you provided. Click it to activate your developer account.
5. Once verified, a **Developer Portal** button appears in the app sidebar (desktop) and mobile UI.
6. Open the **Developer Portal** and click **Generate API Key**. You can have up to 10 active keys.

API keys are free. No credit card. No paywall.

## Authentication

Pass your key on every request via the `X-Api-Key` header (recommended) or as a query parameter:

```
X-Api-Key: your_api_key_here
```

or

```
?api_key=your_api_key_here
```

**Rate limit:** 500 requests / day per key. Resets every 24 hours.

---

## Endpoints

### List Documents

```
GET ?action=documents
```

Returns a paginated list of videos and PDFs from the archive.

**Parameters**

| Name    | Type   | Default | Description                           |
|---------|--------|---------|---------------------------------------|
| `type`  | string | `all`   | Filter: `all`, `video`, or `pdf`      |
| `page`  | int    | `1`     | Page number                           |
| `limit` | int    | `20`    | Results per page (max 50)             |
| `tag`   | string | (none)  | Filter by tag name, case-insensitive  |
| `efta`  | string | (none)  | Filter by source/provenance ID        |

**Example**

```bash
curl "https://exposingepstein.com/backend/api/api_public.php?action=documents&type=video&limit=5" \
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
      "description": "Deposition footage - Palm Beach, 2005",
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

| Name   | Type   | Required | Description              |
|--------|--------|----------|--------------------------|
| `id`   | int    | yes      | Document sequence ID     |
| `type` | string | yes      | `video` or `pdf`         |

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
    "description": "Surveillance footage - Little Saint James",
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

| Name    | Type   | Default | Description                             |
|---------|--------|---------|-----------------------------------------|
| `q`     | string | (none)  | Search query, min 2 characters required |
| `type`  | string | `all`   | Filter: `all`, `video`, or `pdf`        |
| `page`  | int    | `1`     | Page number                             |
| `limit` | int    | `20`    | Results per page (max 50)               |

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
  "data": [ "..." ],
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

All approved tags with document counts, sorted by popularity.

**Parameters**

| Name   | Type   | Default | Description                  |
|--------|--------|---------|------------------------------|
| `type` | string | `all`   | `all`, `video`, or `pdf`     |

**Example**

```bash
curl "https://exposingepstein.com/backend/api/api_public.php?action=tags" \
  -H "X-Api-Key: your_api_key_here"
```

**Response**

```json
{
  "success": true,
  "version": "v1",
  "data": [
    { "name": "maxwell",            "count": 312 },
    { "name": "palm-beach",         "count": 287 },
    { "name": "little-saint-james", "count": 241 },
    { "name": "deposition",         "count": 198 }
  ],
  "total": 1847
}
```

---

### Platform Stats

```
GET ?action=stats
```

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
    "pdfs":   4821,
    "tags":   1847,
    "total":  5804,
    "last_updated": "2026-04-16"
  }
}
```

---

## Error Responses

| HTTP | Code           | Meaning                                    |
|------|----------------|--------------------------------------------|
| 400  | `BAD_REQUEST`  | Missing or invalid parameters              |
| 401  | `NO_API_KEY`   | API key not provided                       |
| 401  | `INVALID_KEY`  | API key does not exist                     |
| 403  | `KEY_DISABLED` | API key has been disabled                  |
| 404  | `NOT_FOUND`    | Document not found                         |
| 429  | `RATE_LIMIT`   | Daily limit reached, resets after 24 hours |

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

# Search PDFs mentioning Maxwell
resp = requests.get(BASE_URL, params={"action": "search", "q": "maxwell", "type": "pdf"}, headers=HEADERS)
for doc in resp.json()["data"]:
    print(f"[{doc['type'].upper()}] id={doc['id']}  tags={doc['tags']}")
```

### JavaScript

```js
const BASE = "https://exposingepstein.com/backend/api/api_public.php";
const KEY  = "your_api_key_here";

async function search(query, type = "all") {
  const url = `${BASE}?action=search&q=${encodeURIComponent(query)}&type=${type}`;
  const res = await fetch(url, { headers: { "X-Api-Key": KEY } });
  return res.json();
}

const results = await search("palm beach");
console.log(`Found ${results.pagination.total} documents`);
results.data.forEach(d => console.log(`${d.type} #${d.id} - ${d.description}`));
```

### curl

```bash
curl -s "https://exposingepstein.com/backend/api/api_public.php?action=search&q=deposition" \
  -H "X-Api-Key: your_key" | python3 -m json.tool
```

---

## What This API Does Not Expose

- User accounts, emails, or any personal data
- Internal database IDs or authentication tokens
- Comments, votes, or community activity
- Unpublished or admin-only content
- Raw file URLs (visit [exposingepstein.com](https://exposingepstein.com) to view files directly)

---

## Terms of Use

- Free for research, journalism, and public interest projects.
- Do not use this API to misrepresent, manipulate, or profit from victims of Jeffrey Epstein.
- We reserve the right to revoke keys that violate these terms.
- The archive is maintained by volunteers. Respect the rate limits.

---

## Contributing

Found a bug or want a new endpoint? Open an [issue](https://github.com/G103L3/epstein-files-api/issues) or submit a pull request.

If this project has been useful to you, consider supporting the platform at [ko-fi.com/exposingepstein](https://ko-fi.com/exposingepstein). Every contribution goes directly to server costs.
