from sqlalchemy.orm import joinedload
from models import Author, Book
from database import SessionLocal

def create_test_data():
    """Создаем тестовые данные"""
    session = SessionLocal()
    
    # Очищаем старые данные
    session.query(Book).delete()
    session.query(Author).delete()
    
    # Создаем авторов и книги
    author1 = Author(name="Лев Толстой")
    author2 = Author(name="Федор Достоевский")
    
    author1.books = [
        Book(title="Война и мир"),
        Book(title="Анна Каренина")
    ]
    
    author2.books = [
        Book(title="Преступление и наказание"), 
        Book(title="Идиот")
    ]
    
    session.add_all([author1, author2])
    session.commit()
    session.close()
    print("✅ Тестовые данные созданы")

def lazy_loading_example():
    """Ленивая загрузка - проблема N+1"""
    print("\n=== ЛЕНИВАЯ ЗАГРУЗКА ===")
    session = SessionLocal()
    
    authors = session.query(Author).all()
    print(f"Найдено авторов: {len(authors)}")
    
    # Проблема N+1: для каждого автора делаем отдельный запрос книг
    for author in authors:
        print(f"Автор: {author.name}")
        for book in author.books:  # Здесь выполняется отдельный SQL запрос
            print(f"  - Книга: {book.title}")
    
    session.close()

def eager_loading_example():
    """Жадная загрузка - один запрос с JOIN"""
    print("\n=== ЖАДНАЯ ЗАГРУЗКА ===")
    session = SessionLocal()
    
    # Все данные загружаются одним запросом
    authors = session.query(Author).options(joinedload(Author.books)).all()
    print(f"Найдено авторов: {len(authors)}")
    
    for author in authors:
        print(f"Автор: {author.name}")
        for book in author.books:  # Книги уже загружены, запросов не происходит
            print(f"  - Книга: {book.title}")
    
    session.close()

if __name__ == "__main__":
    create_test_data()
    lazy_loading_example()
    eager_loading_example()