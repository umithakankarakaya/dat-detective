const CANONICAL_HOST = 'www.datdedektiflik.com';
const REDIRECT_HOSTS = new Set([
  'datdedektiflik.com',
  'datdetective.com',
  'www.datdetective.com',
]);

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const hostname = url.hostname.toLowerCase();

  if (REDIRECT_HOSTS.has(hostname) || (hostname === CANONICAL_HOST && url.protocol === 'http:')) {
    url.hostname = CANONICAL_HOST;
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }

  return context.next();
}
