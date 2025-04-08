from pathlib import Path

from cryptonewsmcp.coindesk import extract_coindesk_news


def test_extract_news():
    news = extract_coindesk_news(Path("tests/testdata/coindesk.html").read_text())
    assert "bitcoin" in news.title.lower()
    assert "tariffs" in news.subtitle.lower()
    assert "Speculation about a Trump tariff delay sent markets swinging wildly during early U.S." in news.content
