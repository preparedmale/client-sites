"""Build a GitHub Pages stub that forwards every old page to the new address."""
import html
import os
from pathlib import Path

NEW = os.environ.get("SITE_BASE", "https://serai-studio.pages.dev").rstrip("/")
SRC, OUT = Path("site"), Path("stub")
OUT.mkdir(exist_ok=True)
for page in SRC.rglob("index.html"):
    rel = page.parent.relative_to(SRC).as_posix()
    url = html.escape(f"{NEW}/" + ("" if rel == "." else rel + "/"))
    dest = OUT / page.relative_to(SRC)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex">'
        f'<link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={url}">'
        f'<title>Serai Studio has moved</title><p>Serai Studio has moved to <a href="{url}">{url}</a>.</p>',
        encoding="utf-8")
(OUT / ".nojekyll").write_text("")
