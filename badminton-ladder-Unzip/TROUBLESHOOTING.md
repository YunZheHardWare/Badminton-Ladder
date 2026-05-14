# If GitHub Pages is showing a blank page

99% of the time, "blank page on GitHub Pages" with a plain HTML site is one of three things below. Run through them in order — first one that matches is your fix.

---

## ① The most likely cause: a folder got nested

When you unzip `badminton-ladder.zip` you get a folder called `badminton-ladder` that **contains** `index.html`, `manifest.webmanifest`, `service-worker.js`, `icons/`, etc.

GitHub Pages serves the **root of the repo**. It looks for `index.html` directly in the repo root. So your repo must end up like this:

```
✅ CORRECT — files at the root
your-repo/
├── index.html
├── manifest.webmanifest
├── service-worker.js
├── icons/
│   └── icon-192.png ...
└── README.md
```

**Not** like this:

```
❌ WRONG — files nested inside a subfolder
your-repo/
└── badminton-ladder/
    ├── index.html
    └── ...
```

If you accidentally uploaded the whole `badminton-ladder` folder (instead of its contents), GitHub Pages serves the repo root, which has nothing in it, and the browser shows a blank page (or a 404).

**Check your repo:** open it on github.com. Do you see `index.html` listed directly, alongside `README.md` and `icons/`? If yes, you're fine. If you see a single `badminton-ladder` folder and nothing else, that's the problem.

**Fix:**
1. On the repo page, click the `badminton-ladder` folder to open it.
2. Select all the files inside it (`index.html`, `service-worker.js`, etc.).
3. Move each one up to the repo root (the easiest way on the web UI is just to delete the folder and re-upload only the **contents**, not the folder itself).
4. Wait a minute for GitHub to redeploy.

---

## ② Pages source is set to the wrong place

In your repo go to **Settings → Pages**. Verify:

- **Source**: should be `Deploy from a branch`
- **Branch**: should be `main` (or `master` — whichever your default is)
- **Folder**: must be `/ (root)` — *not* `/docs`

If the folder is set to `/docs` but your files are in the root, every page will be blank.

After fixing, click Save and wait ~1 minute.

---

## ③ It's still building (or the URL has a typo)

GitHub Pages deployments can take **30 seconds to 5 minutes** the first time, sometimes longer. Check the **Actions** tab in your repo — there will be a "pages build and deployment" workflow. A green checkmark means it's live. A spinning yellow circle means it's still building.

Also double-check the URL. The correct format is:

```
https://YOUR-USERNAME.github.io/REPO-NAME/
```

The trailing slash matters less, but the username and repo name must match exactly. Repo names are case-sensitive in some cases. If the URL in your browser is missing the repo name (or has it spelled wrong), you'll see a blank page or 404.

---

## How to actually diagnose: open the browser console

This will tell you exactly what's wrong in 5 seconds:

**On desktop (Chrome / Safari / Firefox):**
1. Open the broken URL.
2. Right-click anywhere → **Inspect** (or press F12).
3. Click the **Console** tab.
4. Click the **Network** tab and reload the page.

What you'll see:

- **All requests are 404 (red)**: confirms cause ①. Files aren't where Pages expects.
- **`index.html` loaded, but everything else 404**: relative paths broken — usually means the files are there but the icons folder didn't upload. Re-check that the `icons/` folder exists in the repo root.
- **A single 404 specifically for `manifest.webmanifest` or `service-worker.js`**: just that one file is missing — re-upload it.
- **No errors but the page is blank**: cause ② or ③.
- **A red JavaScript error** (like `Unexpected token`): the HTML file got corrupted on upload. Re-upload `index.html`.

**On iPad / iPhone (no built-in dev tools):**
Easier to test on a desktop browser first. If you only have an iPad, open the same URL in any desktop browser (Mac, PC, Chromebook) to diagnose.

---

## Last resort: try a different host

If you've checked all of the above and it still doesn't work, GitHub Pages might just be having a slow day. Try **Netlify Drop** as a 60-second sanity check:

1. Go to https://app.netlify.com/drop
2. Drag the **unzipped folder** (the `badminton-ladder` folder itself — Netlify is happy either way) onto the page.
3. In ~30 seconds you get a working URL.
4. No account, no payment, no DNS setup.

If it works on Netlify but not GitHub Pages, you know it's a GitHub config issue (almost certainly ① or ②), not a problem with the app.

---

## Bonus: how to verify everything works *before* pushing

You can run the app locally to confirm the files are intact:

**Mac**: open Terminal in the unzipped folder, run `python3 -m http.server 8000`, then visit http://localhost:8000 in Safari.

**Windows**: install Python from python.org, then in Command Prompt cd into the folder and run `python -m http.server 8000`, visit http://localhost:8000 in Edge.

If that works, the files are fine and the issue is purely with the GitHub upload structure.
