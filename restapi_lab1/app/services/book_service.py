from app.repository.book_repo import BookRepository

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_books(self, status=None, author=None, sort_by=None):
        books = await self.repo.get_all()
        
        
        if status:
            books = [b for b in books if b["status"] == status]
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]
        
        
        if sort_by in ["title", "year"]:
            books = sorted(books, key=lambda x: x[sort_by])
            
        return books