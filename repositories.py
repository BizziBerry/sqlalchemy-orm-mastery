from typing import List, Optional
from sqlalchemy.orm import Session
from models import Book, Author
from database import SessionLocal

class BookRepository:
    """Repository dlya raboty s knigami"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_book(self, title: str, author_id: int) -> Book:
        """Dobavlenie novoj knigi"""
        book = Book(title=title, author_id=author_id)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def get_books_by_author(self, author_id: int) -> List[Book]:
        """Poluchenie vseh knig avtora po ego ID"""
        return self.db.query(Book).filter(Book.author_id == author_id).all()
    
    def delete_book(self, book_id: int) -> bool:
        """Udalenie knigi po ID"""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False
    
    def get_all_books(self) -> List[Book]:
        """Poluchenie vseh knig (dlya testirovaniya)"""
        return self.db.query(Book).all()

# Fabrika repository
class RepositoryFactory:
    @staticmethod
    def get_book_repository(db: Session) -> BookRepository:
        return BookRepository(db)