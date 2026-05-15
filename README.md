# Badminton Ladder System — Web App (PWA)

A self-contained badminton ladder manager: check-in, court tracking,
challenge queue, scoring, and per-session match history. Installs to the
home screen on iPad and iPhone, runs offline, stores all data on the
device. No login, no server, no fees.

## What's in this folder

```
index.html               — the entire app (UI + logic)
manifest.webmanifest     — PWA metadata (name, icons, theme)
service-worker.js        — caches the app for offline use
icons/                   — app icons (iOS, Android, favicon)
build_icons.py           — regenerate icons (optional; requires Pillow)
```

## Deploy it free with GitHub Pages

1. **Create a new GitHub repository** — any name, e.g. `badminton-ladder`.
   Make it **Public** (Pages is free on public repos).
2. **Upload these files** to the repo root. Either:
   - Drag and drop them into the GitHub web UI ("Add file → Upload files"), or
   - Push with git from your computer.
   Make sure `index.html`, `manifest.webmanifest`, `service-worker.js`, and the `icons/` folder all sit at the **top level** of the repo.
3. **Enable Pages**: in the repo, go to **Settings → Pages**. Under
   "Build and deployment", set **Source** = `Deploy from a branch`,
   **Branch** = `main`, folder = `/ (root)`. Save.
4. Wait ~1 minute. GitHub gives you a URL like
   `https://<your-username>.github.io/badminton-ladder/`.
   Open it on the iPad / iPhone you want to use — that's your live app.

> Other free hosts that work just as well (drag-and-drop, no git needed):
> [Netlify Drop](https://app.netlify.com/drop), [Cloudflare Pages](https://pages.cloudflare.com/),
> [Vercel](https://vercel.com/). Any of them serve the same folder over HTTPS, which is all a PWA needs.

## Install on iPad / iPhone

1. Open the deployed URL in **Safari** (must be Safari — Chrome on iOS
   can't add PWAs to the Home Screen).
2. Tap the **Share** button (the square with the up-arrow at the bottom on
   iPhone, or top-right on iPad).
3. Scroll down and tap **Add to Home Screen**.
4. Confirm — an icon called "Ladder" appears on your home screen.
5. Tap that icon. The app opens **full-screen, no Safari bars**, and from
   then on works **offline** — flight mode, no Wi-Fi, doesn't matter.

A small dark hint banner inside the app reminds you of these steps the
first time you visit in Safari. Dismiss it once and it stays gone.

## Install on Android, Windows, Mac

Same idea — visit the URL in Chrome / Edge / a Chromium browser, and a
"Install app" prompt appears in the address bar.

## Where your data lives

Everything (rosters, archives, careers) is stored in the browser's
`localStorage` on the device that's using the app. There is no cloud sync.

- **Multiple devices**: each device keeps its own data. If you want to run
  the ladder from one iPad consistently, use that iPad consistently.
- **Backup**: if you ever clear Safari data or delete the home-screen app,
  the local data goes with it. (Future enhancement: an export/import
  button for JSON backups — easy to add later if you want it.)
- **Privacy**: nothing leaves the device. Nothing is sent anywhere.

## Updating the app

When you change `index.html` and push the new version to GitHub:

1. Bump the version string at the top of `service-worker.js`:
   ```js
   const CACHE_VERSION = "v1.0.1";   // was "v1.0.0"
   ```
   This forces installed devices to fetch the new files instead of serving
   the cached old ones.
2. Push the changes.
3. On each device that has the app, close and reopen it once.
   The new service worker installs in the background and takes over.
   (If you don't see the change immediately, close and reopen one more time.)

## Touch behaviour

- **Tap** anything to use it — buttons, the pencil ✎ edits, score inputs, etc.
- **Drag to swap players** on the Check-in screen:
  - With a mouse: just drag.
  - On touch: **press and hold** a slot for ~⅓ second, then drag it onto
    another. A short hold prevents accidental drags while you scroll.
- A light vibration (where supported) confirms the drag has started.

## Regenerating the icons

If you want to redesign the icon, edit `build_icons.py` and run:

```
pip install Pillow
python3 build_icons.py
```

It rewrites every file in `icons/`. Then bump `CACHE_VERSION` in the
service worker so devices pull the new images.

## Browser support

- iOS Safari 14+ (iPhone 6s and later)
- iPadOS Safari 14+
- Chrome / Edge / Firefox / Safari on desktop, current versions
- Android Chrome 80+

## Troubleshooting

- **"Add to Home Screen" is missing.** You're not in Safari. Open the URL
  in the actual Safari app (not Chrome, not in-app browsers).
- **App doesn't go offline.** The service worker installs on your *first*
  visit while you're online. After that, force-quit and relaunch the app
  once, then it should work offline.
- **Drag swap isn't working on the iPad.** Make sure you're pressing and
  holding before moving. A quick tap is treated as a select / scroll.
- **Lost my archive.** If localStorage was cleared (private browsing,
  "Clear History and Website Data" in iOS Settings, app uninstalled), the
  data is gone. Recommend keeping the home-screen icon installed and
  not clearing site data for the app's domain.
