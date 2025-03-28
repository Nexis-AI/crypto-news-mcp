# Coindesk MCP

```sh
uv run mcp dev src/coindesk_mcp/server.py
```

```json
{
  "mcpServers": {
    "mcp-server-coindesk": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/narumiruna/mcp-server-coindesk",
        "mcp-server-coindesk"
      ]
    }
  }
}
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
