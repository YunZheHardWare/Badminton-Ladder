/* Badminton Ladder · service worker
   Strategy: cache-first for app shell, with background update.
   Bump CACHE_VERSION every time you deploy a new index.html so the
   service worker fetches the fresh file instead of serving the stale one. */

const CACHE_VERSION = "v1.8.0";
const CACHE_NAME = `badminton-ladder-${CACHE_VERSION}`;

// Files that make up the app shell (relative to the SW scope)
const APP_SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-192.png",
  "./icons/icon-maskable-512.png",
  "./icons/apple-touch-icon.png",
  "./icons/favicon-32.png",
  "./icons/favicon-16.png"
];

// Install: pre-cache the app shell
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean up old caches from previous versions
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k.startsWith("badminton-ladder-") && k !== CACHE_NAME)
          .map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

// Fetch: cache-first for GET requests; ignore everything else
self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  // Ignore non-http(s) (e.g. chrome-extension://)
  const url = new URL(req.url);
  if (url.protocol !== "http:" && url.protocol !== "https:") return;

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) {
        // Update in the background so the next visit is fresh
        fetch(req)
          .then((fresh) => {
            if (fresh && fresh.status === 200 && fresh.type === "basic") {
              caches.open(CACHE_NAME).then((c) => c.put(req, fresh.clone()));
            }
          })
          .catch(() => { /* offline — ignore */ });
        return cached;
      }
      // Not cached: try the network, fall back to index.html for navigations
      return fetch(req)
        .then((res) => {
          if (res && res.status === 200 && res.type === "basic") {
            const copy = res.clone();
            caches.open(CACHE_NAME).then((c) => c.put(req, copy));
          }
          return res;
        })
        .catch(() => {
          if (req.mode === "navigate") return caches.match("./index.html");
          throw new Error("Offline and resource not cached: " + req.url);
        });
    })
  );
});

// Allow the page to trigger an immediate update
self.addEventListener("message", (event) => {
  if (event.data === "SKIP_WAITING") self.skipWaiting();
});
