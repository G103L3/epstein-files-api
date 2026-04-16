"""
Epstein Files API — Python usage examples
Docs: https://github.com/G103L3/epstein-files-api
"""

import requests

API_KEY  = "your_api_key_here"   # get one free: POST ?action=register
BASE_URL = "https://exposingepstein.com/backend/api/api_public.php"
HEADERS  = {"X-Api-Key": API_KEY}


def get_stats():
    """Return archive-wide counts."""
    resp = requests.get(BASE_URL, params={"action": "stats"}, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["data"]


def list_documents(doc_type="all", page=1, limit=20, tag=None):
    """
    List documents from the archive.

    doc_type : "all" | "video" | "pdf"
    tag      : filter by tag name, e.g. "maxwell"
    """
    params = {"action": "documents", "type": doc_type, "page": page, "limit": limit}
    if tag:
        params["tag"] = tag
    resp = requests.get(BASE_URL, params=params, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def search(query, doc_type="all", page=1, limit=20):
    """Full-text search across the archive."""
    params = {"action": "search", "q": query, "type": doc_type, "page": page, "limit": limit}
    resp = requests.get(BASE_URL, params=params, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def get_document(doc_id, doc_type):
    """Fetch a single document by its sequence ID and type."""
    params = {"action": "document", "id": doc_id, "type": doc_type}
    resp = requests.get(BASE_URL, params=params, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["data"]


def get_tags(doc_type="all"):
    """Return all tags sorted by document count."""
    resp = requests.get(BASE_URL, params={"action": "tags", "type": doc_type}, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["data"]


if __name__ == "__main__":
    # --- Stats ---
    stats = get_stats()
    print(f"Archive: {stats['videos']} videos, {stats['pdfs']} PDFs, {stats['tags']} tags")
    print()

    # --- Top 10 tags across the whole archive ---
    tags = get_tags()[:10]
    print("Top 10 tags:")
    for t in tags:
        print(f"  {t['name']:30s} {t['count']} documents")
    print()

    # --- Search PDFs mentioning Maxwell ---
    results = search("maxwell", doc_type="pdf", limit=5)
    print(f"PDFs matching 'maxwell': {results['pagination']['total']} total")
    for doc in results["data"]:
        print(f"  [{doc['type'].upper()}] id={doc['id']}  tags={doc['tags'][:3]}")
    print()

    # --- Browse all videos tagged 'deposition', page by page ---
    page = 1
    total_fetched = 0
    while True:
        batch = list_documents(doc_type="video", tag="deposition", page=page, limit=50)
        docs = batch["data"]
        total_fetched += len(docs)
        print(f"  Page {page}: {len(docs)} videos (fetched {total_fetched} / {batch['pagination']['total']})")
        if not batch["pagination"]["has_more"]:
            break
        page += 1
