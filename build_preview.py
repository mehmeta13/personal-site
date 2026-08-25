#!/usr/bin/env python3
"""Build a single self-contained preview.html from the site files.

Stitches every page into one file with JS screen-switching so the whole
site can be previewed (and navigated) inside the Cowork side panel.
Images and fonts are inlined as data URLs, so the preview renders with
no network access and can be sent as a single file.

Run from inside the site folder:  python3 build_preview.py
Run again after any change to refresh the preview.
"""
import base64
import mimetypes
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent
OUT = SITE / "preview.html"

css = (SITE / "style.css").read_text()

# Map real hrefs -> in-preview screen ids
pages = [
    ("landing", SITE / "index.html"),
    ("thoughts", SITE / "thoughts.html"),
    ("toi", SITE / "toi.html"),
]
for essay in sorted((SITE / "essays").glob("*.html")):
    pages.append((f"essay-{essay.stem}", essay))

href_map = {}
for sid, path in pages:
    rel = path.relative_to(SITE).as_posix()
    href_map[rel] = sid
    href_map["../" + rel] = sid

def body_of(path: Path) -> str:
    html = path.read_text()
    m = re.search(r"<body>(.*)</body>", html, re.S)
    return m.group(1).strip()

sections = []
for sid, path in pages:
    body = body_of(path)
    # rewrite internal links to screen navigation
    for href, target in href_map.items():
        body = body.replace(f'href="{href}"', f'href="#{target}" data-nav="{target}"')
    # inline local images as data URLs so the single-file preview shows them
    def inline_img(m):
        src = m.group(1)
        img_path = (path.parent / src).resolve()
        if img_path.is_file():
            mime = mimetypes.guess_type(img_path.name)[0] or "image/jpeg"
            data = base64.b64encode(img_path.read_bytes()).decode()
            return f'src="data:{mime};base64,{data}"'
        return m.group(0)

    body = re.sub(r'src="([^":]+)"', inline_img, body)
    active = " active" if sid == "landing" else ""
    sections.append(f'<section class="screen{active}" id="{sid}">\n{body}\n</section>')

# inline the self-hosted Inter woff2 as data URLs so the single-file
# preview renders the real font with no network dependency
def font_face(weight):
    fp = SITE / "fonts" / f"inter-latin-{weight}-normal.woff2"
    b64 = base64.b64encode(fp.read_bytes()).decode()
    return (
        "@font-face{font-family:'Inter';font-style:normal;"
        f"font-weight:{weight};font-display:swap;"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
    )

font_css = font_face(400) + font_face(500)

preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Preview — Mehmet Arif Bacaksizlar</title>
<style>
{font_css}
{css}
/* --- preview-only: screen switching --- */
.screen {{ display: none; }}
.screen.active {{ display: block; }}
</style>
</head>
<body>
{chr(10).join(sections)}
<script>
document.addEventListener('click', function (e) {{
  var a = e.target.closest('a[data-nav]');
  if (!a) return;
  e.preventDefault();
  document.querySelectorAll('.screen').forEach(function (s) {{
    s.classList.remove('active');
  }});
  var target = document.getElementById(a.getAttribute('data-nav'));
  if (target) target.classList.add('active');
  window.scrollTo(0, 0);
}});
</script>
</body>
</html>
"""
OUT.write_text(preview)
print(f"wrote {OUT} ({len(preview)} bytes, {len(pages)} screens)")
