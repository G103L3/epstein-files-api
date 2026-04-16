/**
 * Epstein Files API — JavaScript / Node.js usage examples
 * Docs: https://github.com/G103L3/epstein-files-api
 *
 * Works in Node.js 18+ (native fetch) or any modern browser.
 */

const API_KEY = "your_api_key_here"; // get one free: POST ?action=register
const BASE    = "https://exposingepstein.com/backend/api/api_public.php";

async function apiGet(params) {
  const url = new URL(BASE);
  Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  const res = await fetch(url.toString(), { headers: { "X-Api-Key": API_KEY } });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ─── Stats ────────────────────────────────────────────────────────────────────

async function getStats() {
  const { data } = await apiGet({ action: "stats" });
  return data;
}

// ─── List documents ───────────────────────────────────────────────────────────

/**
 * @param {"all"|"video"|"pdf"} type
 * @param {{ page?, limit?, tag?, efta? }} opts
 */
async function listDocuments(type = "all", opts = {}) {
  return apiGet({ action: "documents", type, page: 1, limit: 20, ...opts });
}

// ─── Search ──────────────────────────────────────────────────────────────────

async function search(query, type = "all", page = 1, limit = 20) {
  return apiGet({ action: "search", q: query, type, page, limit });
}

// ─── Single document ─────────────────────────────────────────────────────────

async function getDocument(id, type) {
  const { data } = await apiGet({ action: "document", id, type });
  return data;
}

// ─── Tags ─────────────────────────────────────────────────────────────────────

async function getTags(type = "all") {
  const { data } = await apiGet({ action: "tags", type });
  return data;
}

// ─── Demo ─────────────────────────────────────────────────────────────────────

(async () => {
  // Archive stats
  const stats = await getStats();
  console.log(`Archive: ${stats.videos} videos, ${stats.pdfs} PDFs, ${stats.tags} tags\n`);

  // Top 10 tags
  const tags = (await getTags()).slice(0, 10);
  console.log("Top 10 tags:");
  tags.forEach(t => console.log(`  ${t.name.padEnd(30)} ${t.count} docs`));
  console.log();

  // Search for "palm beach" across everything
  const results = await search("palm beach", "all", 1, 5);
  console.log(`Results for "palm beach": ${results.pagination.total} total`);
  results.data.forEach(d =>
    console.log(`  [${d.type.toUpperCase()}] #${d.id}  tags: ${d.tags.slice(0, 3).join(", ")}`)
  );
  console.log();

  // Paginate all PDFs tagged "deposition"
  let page = 1, fetched = 0;
  while (true) {
    const batch = await listDocuments("pdf", { tag: "deposition", page, limit: 50 });
    fetched += batch.data.length;
    console.log(`  Page ${page}: ${batch.data.length} PDFs (${fetched} / ${batch.pagination.total})`);
    if (!batch.pagination.has_more) break;
    page++;
  }
})();
