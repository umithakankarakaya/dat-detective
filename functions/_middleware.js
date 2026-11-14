const CANONICAL_HOST = 'www.datdetective.com';
const REDIRECT_HOSTS = new Set([
  'datdetective.com',
]);

// Yayına çıkmaması gereken iç/geliştirme dosyaları (kaynak kod, PIN, build betikleri)
const BLOCKED_PATH_RE = /^\/(?:server\.py|readme\.md|wrangler\.toml|tailwind\.config\.js|package(?:-lock)?\.json|scripts\/|src\/|_archive_raw\/|yeni-medya\/|dat evraklar\/|\.git)/i;

async function notFound(context, url) {
  try {
    const page = await context.env.ASSETS.fetch(new URL('/404.html', url.origin));
    return new Response(page.body, {
      status: 404,
      headers: { 'Content-Type': 'text/html; charset=utf-8', 'X-Robots-Tag': 'noindex', 'Cache-Control': 'no-store' },
    });
  } catch (_) {
    return new Response('Not Found', { status: 404, headers: { 'X-Robots-Tag': 'noindex' } });
  }
}

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const hostname = url.hostname.toLowerCase();

  if (REDIRECT_HOSTS.has(hostname) || (hostname === CANONICAL_HOST && url.protocol === 'http:')) {
    url.hostname = CANONICAL_HOST;
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }

  let path;
  try { path = decodeURIComponent(url.pathname); } catch (_) { path = url.pathname; }

  // /Dat/ yansı klasörü sitenin birebir kopyası -> yinelenen içerik olmaması için asıl adrese 301
  if (/^\/dat(?:\/|$)/i.test(path)) {
    const target = new URL(url.toString());
    target.hostname = CANONICAL_HOST;
    target.protocol = 'https:';
    target.pathname = path.replace(/^\/dat/i, '') || '/';
    return Response.redirect(target.toString(), 301);
  }

  if (BLOCKED_PATH_RE.test(path)) {
    return notFound(context, url);
  }

  const response = await context.next();

  // *.pages.dev önizleme adresleri Google'da asıl alan adıyla yarışmasın
  if (hostname.endsWith('.pages.dev')) {
    const res = new Response(response.body, response);
    res.headers.set('X-Robots-Tag', 'noindex, nofollow');
    return res;
  }

  return response;
}
