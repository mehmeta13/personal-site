# Mehmet Arif Bacaksizlar — personal site

**Live at: https://peaceful-douhua-4eb333.netlify.app**

Published on Netlify, July 2026. Public — anyone with that link can read it — but hidden from search engines (see Publishing below). Double-click `Live site.webloc` in this folder to open it.

A minimal static website: dark navy, clean sans-serif, no build tools, no dependencies.

## What's in here

```
index.html        → landing page (name top left, thoughts / t o i in the middle, mail + linkedin bottom left)
thoughts.html     → the essay index (centered titles + dates)
toi.html          → things of interest (framed images with captions)
essays/           → one HTML file per essay
images/           → images used on the toi page
fonts/            → the Inter font files, bundled so the site works offline
style.css         → all styling, shared by every page
robots.txt        → keeps the site out of Google (see Publishing below — don't edit)
Live site.webloc  → double-click to open your published site
build_preview.py  → optional helper that stitches the whole site into one previewable file
CLAUDE.md         → context notes for Claude, so a new session picks up where the last left off
```

## Color palette

Every color is defined once at the top of `style.css` and reused everywhere:

| Color            | Hex       | Used for                                        |
|------------------|-----------|-------------------------------------------------|
| Navy (blue)      | `#0a1930` | page background on every page                   |
| Orange           | `#e8873b` | name, links, essay titles, all back arrows      |
| White            | `#ffffff` | toi frames and caption boxes                    |
| Ivory (text)     | `#e9e6df` | main text — a warm near-white on the navy       |
| Slate (muted)    | `#8fa0b5` | Berkeley CA, dates, secondary text              |

Change a value in the `:root` block of `style.css` and the whole site follows.

## Fonts

- Site-wide: **Inter**, bundled in `fonts/` — nothing is downloaded, so the site looks the same offline.
- toi captions: **Times New Roman**, with the artwork/book name in italics.

## Adding a new essay

1. Duplicate any file in `essays/`, e.g. copy `human-all-too-human.html` to `my-new-essay.html`.
2. In the new file, change the `<title>` at the top, the `<h1>` heading, and the date. Write your paragraphs inside `<p>...</p>` tags; `<em>...</em>` gives italics.
3. In `thoughts.html`, copy one `<li>...</li>` block and update its link, title, and date. Newest on top.

## Adding a thing of interest

1. Put the image file in `images/`.
2. In `toi.html`, copy one whole `<div class="toi-item">...</div>` block and paste it below the last one.
3. Update the `<img src="images/...">` filename and the caption line — keep the name of the work inside `<em>...</em>` so it stays italic.
4. If there is somewhere to buy or watch the thing, keep the pill link to the right of the caption and point its `href` at that page. Rename the label to fit — "Shop" for something to buy, "Watch" for a film. If there is nothing to link to, delete the whole `<a class="shop">...</a>` line and change `toi-caption-row` back to a plain caption.

## Previewing locally

Double-click `index.html`. Everything works offline, fonts included.

## Publishing

Already published, July 2026: **https://peaceful-douhua-4eb333.netlify.app**

To publish a change, go to https://app.netlify.com/drop and drag this whole folder onto the page again. That's the entire workflow — no commands to run, nothing to install.

### Staying out of Google

The site is public — anyone with the link can read it, no password. But it won't show up when someone searches your name. Two files handle that:

- Every page has a `noindex` line in it that tells search engines to skip it. **If you add a new essay, copy an existing page so it inherits that line.**
- `robots.txt` says search engines *are* allowed to visit. This looks backwards but is correct: a search engine has to read the page to see the "skip me" instruction. Blocking it means it never reads the instruction and might list your address anyway. Leave that file alone.

One thing to know: if you ever link the site from LinkedIn or anywhere else that Google indexes, the address becomes findable through that page. The `noindex` only covers your own site.

### Later, if you want a real address

A domain like your own name runs about $12–20 a year and can be pointed at the same Netlify site. Only worth doing if you decide you'd like to be found — a name-shaped domain works against staying unlisted.
