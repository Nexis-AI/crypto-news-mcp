# WIP: Crypto News MCP Server

## TODO

- [x] coindesk
- [ ] [decrypt](https://decrypt.co/)

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
  - Retrieve recent news articles from Coindesk RSS feed
  - Returns a list of articles with title, link, and description
- read_news
  - Read the news article from url
  - Input:
    - url: URL of the Coindesk article
  - Returns the article title, author, and content
