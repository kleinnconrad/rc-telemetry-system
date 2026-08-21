import feedparser
from bs4 import BeautifulSoup
import os
from datetime import datetime

# RSS Feed URL of the specific Reddit thread
RSS_URL = 'https://www.reddit.com/r/rccars/comments/xyz123/my_custom_telemetry_system/.rss'

# Parse Feed
feed = feedparser.parse(RSS_URL)

if feed.bozo:
    print("Error fetching the feed!")
    exit(1)

# Assemble Markdown Header
md_content = "# Reddit Feedback: Live Telemetry System (RSS Sync)\n\n"
md_content += f"**Last Sync:** {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
md_content += "---\n\n"

# Iterate through entries. The first entry is often the post itself, followed by comments.
for entry in feed.entries:
    # Read author (Reddit formats this as /u/username)
    author = entry.get('author', '[Unknown]').replace('/u/', '')
    link = entry.get('link', '')
    
    # The actual text is inside "summary" as HTML
    raw_html = entry.get('summary', '')
    
    # Use BeautifulSoup to remove HTML tags (like <p>, <a>)
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # Extract text and keep line breaks
    text = soup.get_text(separator='\n').strip()
    
    # Add Markdown Blockquote formatting (> )
    text_formatted = text.replace('\n', '\n> ')
    
    md_content += f"**u/{author}** [wrote]({link}):\n"
    md_content += f"> {text_formatted}\n\n"
    md_content += "---\n\n"

# Create target folder and save
os.makedirs('reddit', exist_ok=True)
file_path = 'reddit/reddit_feedback.md'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(md_content)
    
print(f"Successfully saved {len(feed.entries)} entries to {file_path}!")
