import uuid
from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.schemas.book import BookStatus 

class BookModel(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE)
    year = Column(Integer, nullable=False)