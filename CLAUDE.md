# CLAUDE.md — working notes for this project

Read this first. It carries everything a fresh Cowork session needs to pick up
this site without re-asking questions that have already been settled.

## The project

Mehmet Arif Bacaksizlar's personal website — a place to host his essays.
Static HTML + one shared stylesheet. No build step, no framework, no
dependencies, no JavaScript on the live site. Every page is hand-editable and
opens correctly by double-clicking it.

The reference for the look and feel is <https://www.elirousso.com>: minimal,
quiet, nothing decorative.

## File map

```
index.html        landing page
thoughts.html     essay index
toi.html          "things of interest" gallery
essays/           one HTML file per essay
images/           images used on the toi page
fonts/            self-hosted Inter (woff2 + inter.css)
style.css         all styling for every page
robots.txt        crawl directives — read the Publishing section before touching
Live site.webloc  macOS bookmark to the published URL
build_preview.py  builds preview.html — see "Live preview workflow" below
README.md         plain-English guide written for Mehmet
CLAUDE.md         this file
```

## Design tokens

All defined once in the `:root` block of `style.css`. Change them there and the
whole site follows. Never hardcode these values in a page.

| Token          | Hex       | Used for                                          |
|----------------|-----------|---------------------------------------------------|
| `--navy`       | `#0a1930` | page background, everywhere                       |
| `--accent`     | `#e8873b` | name, links, essay titles, back arrows            |
| `--ink`        | `#e9e6df` | body text (warm ivory)                            |
| `--ink-muted`  | `#8fa0b5` | "Berkeley, CA", dates, secondary text             |
| white          | `#ffffff` | toi frames, caption boxes, Shop button outline    |

Fonts: **Inter** site-wide, self-hosted from `fonts/` at weights 400 and 500.
There is no Google Fonts link anywhere and there should not be one — the site
must render identically offline. The only exception to Inter is the toi
captions, which are **Times New Roman**.

## Settled preferences — do not undo these

These were each decided by Mehmet directly, several after seeing an alternative
and rejecting it. Treat them as fixed unless he says otherwise.

- Name sits **top left**, small, in orange. "Berkeley, CA" beneath it in muted
  slate, on the landing and thoughts pages only.
- Landing links ("thoughts" and "t o i") are centered in the page with no
  arrows, circles, borders, or hover chrome.
- "t o i" stays exactly as three spaced letters. An expanded treatment spelling
  out "things of interest" in gray was built and rejected.
- The back arrow is plain `--accent` orange. Gray and gold were both tried and
  rejected — "I want the arrow to have the same color as the orange."
- `thoughts.html` uses `<main class="landing">`, **not** `class="landing page"`.
  This is deliberate: `landing` is what vertically centers the essay list.
  Adding `page` was proposed, previewed, and rejected.
- Essay titles on the index are bulleted, with the date inline to the right.
  Hovering underlines the title only — never the bullet or the date.
- Essay pages have no bottom rule, no footer, and no "back to thoughts" text
  link. The arrow under the name is the only way back.
- Essay body text is justified with hyphenation on, in Inter. Body serif was
  tried early and retired.
- The toi caption box is centered against the image above it using
  `display: grid; grid-template-columns: 1fr auto 1fr` on `.toi-caption-row`.
  Do not convert this back to flex — flex centers the caption and Shop button
  as a unit, which visibly shifts the caption left.
- The Shop button is a white outlined pill with white text and arrow on the
  navy background.

## Adding an essay

1. Copy an existing file in `essays/` to a new kebab-case filename.
2. Update the `<title>`, the `<h1>`, and the `.essay-date`. Body goes in `<p>`
   tags; `<em>` for italics. Use curly quotes (`&ldquo;` `&rdquo;` `&rsquo;`)
   and em dashes (`&mdash;`) rather than straight ASCII. Copying an existing
   file keeps the `noindex` meta tag — see Publishing for why that matters.
3. Add one `<li>` to the `.thought-index` list in `thoughts.html`, newest at
   the top, matching the title and date exactly.

Nothing else needs touching — no index to regenerate, no config.

If Mehmet pastes essay text without a title, propose one drawn from the piece
itself and tell him it is easy to change rather than blocking on the question.

## Adding a thing of interest

1. Put the image in `images/`. Prefer a reasonably high-resolution file; a
   low-res one was caught and replaced once already.
2. Copy a whole `<div class="toi-item">` block in `toi.html` and update the
   `<img>` src, alt, and its intrinsic `width`/`height` attributes — those
   attributes prevent layout shift and must match the real pixel dimensions.
3. Write the caption with the name of the work in `<em>`.
4. Include a `.shop` link only if there is somewhere to send people. The class
   stays `.shop` whatever the label says — the label itself matches the
   destination ("Shop" for a book, "Watch" for a film on Apple TV).

Current images: `bull.jpg` (700×460), `zarathustra.jpg` (652×1000),
`amarcord.jpg` (1400×992, downscaled from a 2560px original).

## Live preview workflow

Mehmet works by looking at a rendered preview in the Cowork side panel and
giving feedback in chat. The loop is: edit files → rebuild the preview →
send it → he responds → repeat. Keep iterations small and show the result
every time rather than batching several changes.

```
python3 build_preview.py
```

Run it from inside this folder. It stitches every page into a single
self-contained `preview.html` with JS screen-switching, base64-inlining the
images and the Inter woff2 files so it renders with no network access. New
essays are picked up automatically from `essays/*.html`.

Deliver `preview.html` with `SendUserFile`, then pin it with
`mcp__remote-devices__update_artifact` using the artifact id
**`mehmet-personal-site`** so it stays in the side panel across sessions. If
that id does not exist yet on the device, use `create_artifact` to make it.

For verification screenshots, Playwright with Chromium at
`/opt/pw-browsers/chromium` renders the real files directly via `file://` URLs.

## Publishing — public but unlisted

**Live URL: https://peaceful-douhua-4eb333.netlify.app**
Deployed to Netlify by drag-and-drop, July 2026. Verified serving the noindex
tag and the crawl-allowing robots.txt. To publish a change, Mehmet drags the
folder onto <https://app.netlify.com/drop> again — there is no CI, no git
remote, no deploy command.

The site is fully public: no password, no login, anyone with the link can read
it. What Mehmet does not want is for it to surface when someone googles his
name. That is handled by two files working together, and it is easy to break
by "fixing" one of them:

- Every page carries `<meta name="robots" content="noindex, nofollow">` in its
  `<head>`. **Any new page must have it too** — an essay added without it is
  the one page that can end up in search results.
- `robots.txt` deliberately **allows** crawling. Do not change it to
  `Disallow: /`. A crawler has to fetch a page to read its noindex tag;
  blocking it means the tag is never seen and Google can still list the bare
  URL from an external link. Blocking makes indexing *more* likely, not less.

Host: **Netlify Drop** — drag the folder onto <https://app.netlify.com/drop>,
live in seconds on a random subdomain, free, no build step. GitHub Pages works
equally well if he ever prefers it. A custom domain (~$12–20/yr) can be pointed
at either later; suggest that only if he decides he *wants* to be found, since
a name-shaped domain is the opposite of unlisted.

Worth flagging to him if it ever becomes relevant: noindex keeps the site out
of search, but linking it from LinkedIn or another indexed page makes the URL
itself public and discoverable by anyone reading that page.

## Working notes

- Pasted images have historically not arrived as files in this project. When
  Mehmet shares an image, expect to pull it from his Downloads folder through
  the device bridge instead. `device_list_dir` on Downloads overflows the token
  limit, so parse the result with python and sort by `mtimeMs` descending.
- He gives feedback in short, concrete notes. Make the change, show it, and
  keep the explanation to a sentence or two — he is looking at the result, not
  reading a description of it.
