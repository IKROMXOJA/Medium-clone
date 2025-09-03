from pydantic import BaseModel
from typing import Optional

class ArticleCreate(BaseModel):
    title: str
    content: str
    published: bool = False

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    author_id: int
    image_path: Optional[str] = None

    class Config:
        from_attributes = True
