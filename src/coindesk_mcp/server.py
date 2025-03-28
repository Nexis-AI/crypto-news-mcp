from typing import Final

import feedparser
from mcp.server.fastmcp import FastMCP

from coindesk_mcp.page import extract_newspage
from coindesk_mcp.utils import fetch_text_from_url

COINDESK_RSS_URL: Final[str] = "https://www.coindesk.com/arc/outboundfeeds/rss"


mcp = FastMCP("MCP Server Coindesk")


@mcp.tool()
async def get_news_content(url: str) -> str:
    """
    Fetches and extracts the content of a news article from a given URL.

    This asynchronous function retrieves the HTML content from the specified URL,
    extracts the news page content using the extract_newspage function,
    and returns the extracted content as a string.

    Args:
        url (str): The URL of the news article to fetch and extract.

    Returns:
        str: The extracted content of the news article as a string.

    Raises:
        Any exceptions that might be raised by fetch_text_from_url or extract_newspage.
    """
    html = await fetch_text_from_url(url)
    newspage = extract_newspage(html)
    return str(newspage)


@mcp.tool()
async def list_rss_feed() -> str:
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
