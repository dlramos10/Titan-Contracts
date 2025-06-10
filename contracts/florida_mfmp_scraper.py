
import feedparser
from datetime import datetime

def fetch_mfmp_bids():
    feed_url = "https://www.myfloridamarketplace.com/feed/rss.xml"
    feed = feedparser.parse(feed_url)
    results = []

    for entry in feed.entries[:20]:  # Limit to latest 20 for performance
        results.append({
            "id": entry.id if hasattr(entry, "id") else entry.link,
            "title": entry.title,
            "url": entry.link,
            "source": "MyFloridaMarketPlace",
            "agency": "Florida Department",
            "publishDate": entry.published if hasattr(entry, "published") else "",
            "deadline": "",
            "naics": ""
        })
    return results
