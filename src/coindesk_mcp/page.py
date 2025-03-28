from datetime import datetime

import dateutil.parser
from bs4 import BeautifulSoup
from pydantic import BaseModel
from pydantic import Field


class CoindeskNewsPage(BaseModel):
    title: str | None = Field(default=None)
    subtitle: str | None = Field(default=None)
    content: str | None = Field(default=None)
    author: str | None = Field(default=None)
    published_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)

    def __str__(self) -> str:
        result = [f"Title: {self.title}"]

        if self.subtitle:
            result.append(f"Subtitle: {self.subtitle}")

        if self.author:
            result.append(f"By: {self.author}")

        dates = []
        if self.published_at:
            dates.append(f"Published: {self.published_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.updated_at:
            dates.append(f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

        if dates:
            result.append(" | ".join(dates))

        if self.content:
            content_preview = self.content[:150] + "..." if len(self.content) > 150 else self.content
            result.append(f"\n{content_preview}")

        return "\n".join(result)


def extract_title(soup: BeautifulSoup) -> str | None:
    title_tag = soup.select_one("h1.font-headline-lg.font-medium")
    if title_tag is None:
        return None
    return title_tag.get_text().strip()


def extract_subtitle(soup: BeautifulSoup) -> str | None:
    subtitle_tag = soup.select_one("h2.font-headline-xs.text-charcoal-600")
    if subtitle_tag is None:
        return None
    return subtitle_tag.get_text().strip()


def extract_content(soup: BeautifulSoup) -> str | None:
    results = soup.select("div.document-body.font-body-lg")
    return "\n".join([result.get_text().strip() for result in results])


def extract_author(soup: BeautifulSoup) -> str | None:
    result = soup.select_one("h5.font-headline-sm.font-medium")
    if result is None:
        return None
    return result.get_text().strip()


def extract_newspage(html: str) -> CoindeskNewsPage:
    soup = BeautifulSoup(html, "html.parser")

    published_at, updated_at = extract_published_at(soup)

    return CoindeskNewsPage(
        title=extract_title(soup),
        subtitle=extract_subtitle(soup),
        content=extract_content(soup),
        author=extract_author(soup),
        published_at=published_at,
        updated_at=updated_at,
    )


def extract_published_at(soup: BeautifulSoup) -> tuple[datetime | None, datetime | None]:
    tag = soup.select_one("div.font-metadata.flex.gap-4.text-charcoal-600.flex-col.md\\:block")
    if tag is None:
        return None, None

    published_at = None
    updated_at = None

    results = tag.select("span")
    for result in results:
        date_str = result.get_text().strip()
        if "Published" in date_str:
            published_at = dateutil.parser.parse(date_str.removeprefix("Published "))
        elif "Updated" in date_str:
            updated_at = dateutil.parser.parse(date_str.removeprefix("Updated "))
        else:
            published_at = dateutil.parser.parse(date_str)
    return published_at, updated_at
