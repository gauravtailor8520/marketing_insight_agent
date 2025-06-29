# File: blogs/fetch_blogs.py
"""Fetch or load sample marketing blog content for indexing."""

import os
from pathlib import Path


SAMPLE_BLOGS = [
    {
        "title": "5 Best Ad Copy Tips for Summer Campaigns",
        "url": "https://blog.hubspot.com/marketing/ad-copy-tips",
        "content": (
            "Use urgency in headlines. Include emojis where appropriate. Localize copy for target audience."
            " Focus on benefits not just features. Run A/B tests regularly to optimize copy performance."
        )
    },
    {
        "title": "Why CTR Dips and How to Fix It",
        "url": "https://www.wordstream.com/blog/ws/2021/03/02/low-ctr",
        "content": (
            "CTR may dip due to ad fatigue, irrelevant targeting, or weak creatives. Refresh ads weekly, improve targeting,"
            " and test new formats. Add trust signals and social proof to regain engagement."
        )
    },
    {
        "title": "Top 10 Email Campaign Tactics That Work",
        "url": "https://mailchimp.com/resources/email-marketing-best-practices/",
        "content": (
            "Segment your audience carefully. Personalize subject lines. Strong CTAs drive clicks."
            " Optimize send times and ensure mobile responsiveness."
        )
    }
]



# Save mock data to local .txt files (you can later replace this with scraping logic)
def save_sample_blogs(folder="blogs/data"):
    os.makedirs(folder, exist_ok=True)
    for blog in SAMPLE_BLOGS:
        path = Path(folder) / f"{blog['title'].replace(' ', '_')}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(blog["content"])


if __name__ == "__main__":
    save_sample_blogs()