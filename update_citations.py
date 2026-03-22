"""
update_citations.py
-------------------
Fetches citation counts from OpenAlex for every publication in index.html
(matched by DOI) and updates the "Cited by X" badges.

OpenAlex is free, requires no API key, and reports counts much closer
to Google Scholar than Semantic Scholar does.

Usage:
    python3 update_citations.py

- Adds a citation badge if one doesn't exist yet.
- Updates the count if a badge already exists.
- Skips a paper gracefully if OpenAlex doesn't have it.
- Also updates the total citation count in the bento card and
  the publications section tag at the top of the page.
- Safe to re-run at any time.
"""

import re
import time
import urllib.request
import urllib.error
import json

HTML_FILE = "index.html"
API_BASE  = "https://api.openalex.org/works/doi:{doi}"
DELAY_SEC = 0.2   # OpenAlex allows up to 10 req/sec for polite crawling

CITE_BADGE_SVG = (
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2.5">'
    '<path d="M7 7l5 5-5 5M13 7l5 5-5 5"/></svg>'
)

CITE_BADGE_TEMPLATE = (
    '<span class="cite-badge">{svg} Cited by {count}</span>'
).format(svg=CITE_BADGE_SVG, count="{count}")


def fetch_citation_count(doi: str) -> int | None:
    url = API_BASE.format(doi=doi)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "citation-updater/1.0 (mailto:ecjywork@gmail.com)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("cited_by_count")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  [not found] {doi}")
        else:
            print(f"  [HTTP {e.code}] {doi}")
    except Exception as e:
        print(f"  [error] {doi}: {e}")
    return None


def main():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Split into pub-stats blocks so we can update each independently
    # Each block runs from <div class="pub-stats"> to </div>
    stats_pattern = re.compile(
        r'(<div class="pub-stats">)(.*?)(</div>)',
        re.DOTALL
    )

    doi_in_block = re.compile(r'href="https://doi\.org/([^"]+)"')
    cited_badge  = re.compile(r'<span class="cite-badge">.*?Cited by \d+.*?</span>')
    before_btn   = re.compile(r'(<button class="pub-summary-toggle")')

    updated = skipped = not_found = 0

    def process_block(m):
        nonlocal updated, skipped, not_found
        block = m.group(2)

        doi_match = doi_in_block.search(block)
        if not doi_match:
            return m.group(0)

        doi = doi_match.group(1)
        print(f"Fetching: {doi}")
        count = fetch_citation_count(doi)
        time.sleep(DELAY_SEC)

        if count is None:
            not_found += 1
            return m.group(0)   # leave unchanged

        badge_html = CITE_BADGE_TEMPLATE.format(count=count)

        if cited_badge.search(block):
            # Update existing badge
            new_block = cited_badge.sub(badge_html, block)
            updated += 1
        else:
            # Insert badge before the Summary button
            if before_btn.search(block):
                new_block = before_btn.sub(badge_html + r"\n                            \1", block)
                updated += 1
            else:
                skipped += 1
                return m.group(0)

        return m.group(1) + new_block + m.group(3)

    new_html = stats_pattern.sub(process_block, html)

    # Recount total citations from all badges and update the top section
    all_counts = [int(x) for x in re.findall(r'Cited by (\d+)', new_html)]
    total = sum(all_counts)
    print(f"\nTotal citations across all badges: {total}")

    # Update bento card number
    new_html = re.sub(
        r'(<div class="bento-num"[^>]*>)\d+(</div>\s*<div class="bento-label">Total Citations)',
        rf'\g<1>{total}\2',
        new_html
    )
    # Update publications section tag
    new_html = re.sub(
        r'(\d+) Citations(</span>.*?38 Articles)',
        rf'{total} Citations\2',
        new_html,
        flags=re.DOTALL
    )

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"Done. Updated: {updated} | Not found / skipped: {not_found + skipped}")


if __name__ == "__main__":
    main()
