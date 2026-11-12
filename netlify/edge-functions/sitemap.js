// Serves the built sitemap.xml with the Soro blog posts appended.
//
// Soro publishes posts most days, outside this repo, and they live at
// /blog/?post=<slug> (the same URL the embed sets as canonical). Reading them
// here on request keeps the sitemap current without a rebuild or a deploy.
// If Soro is slow or down, the static sitemap goes out unchanged.

const API = "https://app.trysoro.com/api/embed/8bb533f4-55ea-4c1e-b09a-843dcf0f3f55/articles";
const SITE = "https://morgenruf.dev";

async function soroEntries() {
  const seen = new Map();
  for (let page = 1, total = 1; page <= total && page <= 50; page++) {
    const res = await fetch(`${API}?page=${page}`, { signal: AbortSignal.timeout(4000) });
    if (!res.ok) throw new Error(`Soro returned ${res.status}`);
    const data = await res.json();
    if (data.page !== page) break;
    total = data.totalPages || 1;
    for (const a of data.articles || []) {
      if (a.slug && !seen.has(a.slug)) seen.set(a.slug, (a.isoDate || "").slice(0, 10));
    }
  }
  return [...seen].map(([slug, day]) =>
    `  <url>\n    <loc>${SITE}/blog/?post=${encodeURIComponent(slug)}</loc>\n` +
    (day ? `    <lastmod>${day}</lastmod>\n` : "") + "  </url>\n").join("");
}

export default async (request, context) => {
  const xml = await (await context.next()).text();
  let extra = "";
  try {
    extra = await soroEntries();
  } catch (err) {
    console.error(`sitemap: Soro posts left out: ${err.message}`);
  }
  return new Response(xml.replace("</urlset>", extra + "</urlset>"), {
    headers: {
      "content-type": "application/xml; charset=utf-8",
      "cache-control": "public, max-age=3600",
    },
  });
};

export const config = { path: "/sitemap.xml" };
