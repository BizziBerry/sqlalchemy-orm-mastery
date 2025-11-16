from repositories import RepositoryFactory
from database import SessionLocal

def test_repository():
    print("=== TESTIRUEM REPOSITORY PATTERN ===")
    
    db = SessionLocal()
    
    try:
        book_repo = RepositoryFactory.get_book_repository(db)
        
        print("1. Poluchaem vse knigi:")
        all_books = book_repo.get_all_books()
        print(f"   Vsego knig: {len(all_books)}")
        
        print("2. Poluchaem knigi avtora (ID: 1):")
        author_books = book_repo.get_books_by_author(1)
        print(f"   Knig u avtora: {len(author_books)}")
        for book in author_books:
            print(f"     - {book.title}")
            
        print("3. Udalaem knigu:")
        if author_books:
            result = book_repo.delete_book(author_books[0].id)
            print(f"   Rezultat udaleniya: {result}")
            
        print("4. Proverka posle udaleniya:")
        author_books_after = book_repo.get_books_by_author(1)
        print(f"   Ostalos knig: {len(author_books_after)}")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_repository()