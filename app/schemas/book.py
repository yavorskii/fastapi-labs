from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List

class BookStatus(str, Enum):
    AVAILABLE = "наявна"
    BORROWED = "видана"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: BookStatus = BookStatus.AVAILABLE
    year: int = Field(..., gt=0)

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: str

class BookListResponse(BaseModel):
    items: List[Book]
    total: int
    limit: int
    offset: int