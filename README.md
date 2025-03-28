# Coindesk MCP

```sh
uv run mcp dev src/coindesk_mcp/server.py
```

## Components

### Tools

- recent_news
  - Retrieve recent news articles from Coindesk RSS feed
  - Returns a list of articles with title, link, and description
- read_news
  - Read the news article from url
  - Input:
    - url: URL of the Coindesk article
  - Returns the article title, author, and content
