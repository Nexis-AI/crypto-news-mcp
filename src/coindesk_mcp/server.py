from typing import Final

import feedparser
from mcp.server.fastmcp import FastMCP

from coindesk_mcp.page import extract_newspage
from coindesk_mcp.utils import fetch_text_from_url

COINDESK_RSS_URL: Final[str] = "https://www.coindesk.com/arc/outboundfeeds/rss"


INSTRUCTIONS: Final[str] = """
This MCP server provides access to CoinDesk cryptocurrency and blockchain news content.

Available tools:
- list_rss_feed: Fetches the latest news articles from CoinDesk's RSS feed
- read_news: Retrieves the full content of a specific news article using its URL

Usage guidelines:
1. Use list_rss_feed to obtain recent headlines, links, timestamps, and article summaries
2. Use read_news with an article URL to fetch the complete article content
3. Process and present the news data according to your application requirements

Data handling:
- The RSS feed data includes article titles, links, publication timestamps, and summaries
- Full article content may contain text, embedded media references, and formatting elements
- Citation is recommended when republishing any content, referencing CoinDesk as the source

Rate limits and performance considerations:
- Implement appropriate caching mechanisms for frequently accessed content
- Avoid excessive requests to the underlying CoinDesk services
"""


mcp = FastMCP("MCP Server Coindesk", instructions=INSTRUCTIONS)


@mcp.tool()
async def read_news(url: str) -> str:
    """
    Retrieves news content from a specified URL.

    This function fetches the HTML content from the given URL, extracts the news
    content from the HTML, and returns it as a string.

    Args:
        url (str): The URL of the news page to read.

    Returns:
        str: The extracted news content as a string.

    Raises:
        Any exceptions that might be raised by the fetch_text_from_url or extract_newspage functions.
    """
    html = await fetch_text_from_url(url)
    newspage = extract_newspage(html)
    return str(newspage)


@mcp.tool()
async def list_recent_news() -> str:
    """
    Fetches and parses the CoinDesk RSS feed, returning a formatted string of feed entries.

    This async function retrieves the RSS feed from the COINDESK_RSS_URL, parses it,
    and formats the entries with title, link, update time, and summary information.

    Returns:
        str: A string containing formatted RSS feed entries, separated by '---'.
            Each entry includes the title, link, update timestamp, and summary.

    Raises:
        Any exceptions that might be raised by fetch_text_from_url.
    """
    text = await fetch_text_from_url(COINDESK_RSS_URL)
    feed = feedparser.parse(text)
    return "\n---\n".join(
        f"{entry['title']}\n{entry['link']}\n{entry['updated']}\n{entry['summary']}" for entry in feed["entries"]
    )
