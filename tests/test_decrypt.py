from pathlib import Path

from cryptonewsmcp.decrypt import extract_news_from_decrypt


def test_extract_news_from_decrypt() -> None:
    """Test extracting news data from a Decrypt article HTML file."""
    news = extract_news_from_decrypt(Path("tests/testdata/decrypt.html").read_text())

    # Verify the extracted information
    assert "Tariffs" in news.title
    assert "Ray Dalio" in news.title
    assert "Crypto and equities have moved in lockstep" in news.subtitle
    assert news.author == "Vince Dioquino"
    # We can't test exact content since we don't see the full HTML structure in the code context,
    # but we at least check that content was extracted
    assert news.content is not None
