# WIP: Crypto News MCP Server

## TODO

- [x] coindesk
- [x] [decrypt](https://decrypt.co/)

## Usage

```json
{
  "mcpServers": {
    "cryptonewsmcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/narumiruna/crypto-news-mcp",
        "cryptonewsmcp"
      ]
    }
  }
}
```

## Components

### Tools

- recent_news
  - Fetches latest crypto news from specified site
  - Input:
    - site: Source site ("coindesk" or "decrypt")
  - Returns formatted list of news entries with titles, links, dates and summaries
- read_news
  - Gets article content from URL
  - Input:
    - url: Article URL to retrieve
  - Returns formatted article content
