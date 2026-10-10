"""Fetch the comments of the project's Reddit thread and store them as Markdown.

The thread's RSS feed is parsed and each entry is written as a blockquote to
reddit/reddit_feedback.md. The file is only rewritten when the comments have
changed, so the sync timestamp alone never produces a new commit.

Run:  python scripts/fetch_reddit.py
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import feedparser
from bs4 import BeautifulSoup

POST_ID = "1s9dydh"
THREAD_URL = f"https://www.reddit.com/r/esp32/comments/{POST_ID}/"
RSS_URL = f"{THREAD_URL}.rss"

# Reddit rejects requests that use a generic client User-Agent
USER_AGENT = "GitHubAction:carten-telemetry-rss-sync:v1.1"

OUTPUT = Path(__file__).resolve().parent.parent / "reddit" / "reddit_feedback.md"
SYNC_LINE = re.compile(r"^\*\*Last sync:\*\*.*$", re.MULTILINE)
# Zero-width spaces from the Reddit editor and emojis (repository style rule)
STRIP_CHARS = re.compile("[​️☀-➿\U0001f300-\U0001faff]")


def entry_text(html):
    """Return the comment body as plain text, one paragraph per line."""
    soup = BeautifulSoup(STRIP_CHARS.sub("", html), "html.parser")
    # The comment itself sits in <div class="md">; everything after it is
    # Reddit's "submitted by ... [link] [comments]" footer
    body = soup.find("div", class_="md") or soup
    blocks = [el for el in body.find_all(["p", "li", "pre"])
              if not el.find_parent(["li", "pre"])]
    if not blocks:
        return " ".join(body.get_text().split())
    paragraphs = []
    for el in blocks:
        if el.name == "pre":
            paragraphs.append(el.get_text().rstrip())
        else:
            prefix = "- " if el.name == "li" else ""
            paragraphs.append(prefix + " ".join(el.get_text().split()))
    return "\n\n".join(p for p in paragraphs if p)


def build_markdown(entries, synced_at):
    lines = [
        "# Reddit Feedback",
        "",
        f"Comments from the r/esp32 thread [{POST_ID}]({THREAD_URL}), "
        "synchronized via RSS by `scripts/fetch_reddit.py`.",
        "",
        f"**Last sync:** {synced_at}",
        "",
        "---",
        "",
    ]
    for entry in entries:
        author = entry.get("author", "[unknown]").replace("/u/", "")
        quoted = "\n".join(f"> {line}".rstrip() for line in entry_text(entry.get("summary", "")).splitlines())
        lines += [f"**u/{author}** [wrote]({entry.get('link', THREAD_URL)}):", "", quoted, "", "---", ""]
    return "\n".join(lines)


def main():
    feed = feedparser.parse(RSS_URL, agent=USER_AGENT)
    if feed.get("status") != 200 or not feed.entries:
        print(f"Error fetching the feed (HTTP status {feed.get('status')}, {len(feed.entries)} entries)")
        sys.exit(1)

    synced_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    content = build_markdown(feed.entries, synced_at)

    if OUTPUT.exists():
        old = OUTPUT.read_text(encoding="utf-8")
        if SYNC_LINE.sub("", old) == SYNC_LINE.sub("", content):
            print("No new comments. File left unchanged.")
            return

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Saved {len(feed.entries)} entries to {OUTPUT}")


if __name__ == "__main__":
    main()
