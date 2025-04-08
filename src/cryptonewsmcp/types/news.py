from pydantic import BaseModel


class News(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    content: str | None = None
    author: str | None = None
