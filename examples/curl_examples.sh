#!/usr/bin/env bash
# Epstein Files API — curl examples
# Docs: https://github.com/G103L3/epstein-files-api

API_KEY="your_api_key_here"
BASE="https://exposingepstein.com/backend/api/api_public.php"

# ─── Register for an API key ─────────────────────────────────────────────────

curl -s -X POST "$BASE?action=register" \
  -H "Content-Type: application/json" \
  -d '{"app_name":"my-tool","email":"you@example.com","origin_url":"https://mytool.com"}' \
  | python3 -m json.tool

# ─── Stats ───────────────────────────────────────────────────────────────────

curl -s "$BASE?action=stats" \
  -H "X-Api-Key: $API_KEY" \
  | python3 -m json.tool

# ─── List 10 videos from page 1 ──────────────────────────────────────────────

curl -s "$BASE?action=documents&type=video&limit=10&page=1" \
  -H "X-Api-Key: $API_KEY" \
  | python3 -m json.tool

# ─── List PDFs tagged "deposition" ───────────────────────────────────────────

curl -s "$BASE?action=documents&type=pdf&tag=deposition&limit=20" \
  -H "X-Api-Key: $API_KEY" \
  | python3 -m json.tool

# ─── Search for "maxwell" in PDFs ────────────────────────────────────────────

curl -s "$BASE?action=search&q=maxwell&type=pdf" \
  -H "X-Api-Key: $API_KEY" \
  | python3 -m json.tool

# ─── Get a single video (id=42) ──────────────────────────────────────────────

curl -s "$BASE?action=document&id=42&type=video" \
  -H "X-Api-Key: $API_KEY" \
  | python3 -m json.tool

# ─── List all tags (sorted by count) ─────────────────────────────────────────

curl -s "$BASE?action=tags" \
  -H "X-Api-Key: $API_KEY" \
  | python3 -m json.tool

# ─── API key as query param (alternative) ────────────────────────────────────

curl -s "$BASE?action=stats&api_key=$API_KEY" \
  | python3 -m json.tool
