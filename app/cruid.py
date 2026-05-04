from sqlalchemy.future import select
from sqlalchemy import asc
from app.models import Book
from sqlalchemy.ext.asyncio import AsyncSession

async def get_books_cursor(db: AsyncSession, cursor: Optional[int], size: int):
    query = select(Book).order_by(asc(Book.id)).limit(size)
    
    if cursor is not None:
        query = query.where(Book.id > cursor)
    
    result = await db.execute(query)
    books = result.scalars().all()
    
    next_cursor = books[-1].id if len(books) == size else None
    
    return books, next_cursor