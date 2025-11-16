import logging
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import text, func
from models import Author, Book
from database import SessionLocal

# Настройка логирования SQL-запросов
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def demonstrate_logging():
    """Демонстрация логирования SQL-запросов"""
    print("=== LOGIROVANIE SQL-ZAPROSOV ===")
    
    session = SessionLocal()
    
    try:
        print("1. Prostoj zapros:")
        authors = session.query(Author).all()
        print(f"   Najdeno avtorov: {len(authors)}")
        
        print("2. Zapros so svjazjami:")
        authors_with_books = session.query(Author).options(joinedload(Author.books)).all()
        for author in authors_with_books:
            print(f"   Avtor: {author.name}, knig: {len(author.books)}")
            
    finally:
        session.close()

def analyze_loading_strategies():
    """Анализ различных стратегий загрузки"""
    print("\n=== ANALIZ STRATEGIJ ZAGRUZKI ===")
    
    session = SessionLocal()
    
    try:
        print("1. Lenivaja zagruzka (problem N+1):")
        authors = session.query(Author).all()
        total_books = 0
        for author in authors:
            books_count = len(author.books)  # Otdelnyj zapros dlja kazhdogo avtora
            total_books += books_count
        print(f"   Vsego knig: {total_books}")
        
        print("2. Zhadnaja zagruzka s JOIN:")
        authors = session.query(Author).options(joinedload(Author.books)).all()
        total_books = 0
        for author in authors:
            books_count = len(author.books)  # Net dopolnitelnyh zaprosov
            total_books += books_count
        print(f"   Vsego knig: {total_books}")
        
        print("3. Zhadnaja zagruzka s SELECT IN:")
        authors = session.query(Author).options(selectinload(Author.books)).all()
        total_books = 0
        for author in authors:
            books_count = len(author.books)  # Net dopolnitelnyh zaprosov
            total_books += books_count
        print(f"   Vsego knig: {total_books}")
            
    finally:
        session.close()

def sqlalchemy_core_example():
    """Пример использования SQLAlchemy Core для сложных запросов"""
    print("\n=== SQLALCHEMY CORE - SLOZhNYE ZAPROSY ===")
    
    session = SessionLocal()
    
    try:
        # Slozhnyj agregirujushhij zapros s ispol'zovaniem Core
        query = text("""
            SELECT 
                a.name as author_name,
                COUNT(b.id) as book_count,
                AVG(LENGTH(b.title)) as avg_title_length
            FROM authors a
            LEFT JOIN books b ON a.id = b.author_id
            GROUP BY a.id, a.name
            HAVING COUNT(b.id) > 0
            ORDER BY book_count DESC
        """)
        
        result = session.execute(query)
        
        print("Statistika po avtoram:")
        for row in result:
            print(f"   Avtor: {row.author_name}")
            print(f"     Kollichestvo knig: {row.book_count}")
            print(f"     Srednjaja dlina nazvanija: {row.avg_title_length:.1f} simvolov")
            print()
            
    finally:
        session.close()

def mixed_orm_core_usage():
    """Совместное использование ORM и Core"""
    print("\n=== SOVMESTNOE ISPOL'ZOVANIE ORM I CORE ===")
    
    session = SessionLocal()
    
    try:
        # Ispol'zuem ORM dlja prostyh operacij
        print("1. ORM - prostye operacii:")
        authors = session.query(Author).all()
        print(f"   Vsego avtorov: {len(authors)}")
        
        # Ispol'zuem Core dlja slozhnoj agregacii
        print("2. Core - slozhnaja statistika:")
        stmt = text("""
            SELECT author_id, COUNT(*) as book_count 
            FROM books 
            GROUP BY author_id
            ORDER BY book_count DESC
        """)
        
        book_stats = session.execute(stmt).fetchall()
        print("   Kollichestvo knig po avtoram:")
        for author_id, count in book_stats:
            author = session.query(Author).get(author_id)
            print(f"     {author.name}: {count} knig")
            
        # Kombinirovannyj podhod
        print("3. Kombinirovannyj podhod:")
        for author in authors:
            # ORM dlja poluchenija ob#ekta
            author_name = author.name
            # Core dlja bystrogo podscheta
            count_stmt = text("SELECT COUNT(*) FROM books WHERE author_id = :author_id")
            book_count = session.execute(count_stmt, {"author_id": author.id}).scalar()
            print(f"     {author_name}: {book_count} knig")
            
    finally:
        session.close()

if __name__ == "__main__":
    demonstrate_logging()
    analyze_loading_strategies() 
    sqlalchemy_core_example()
    mixed_orm_core_usage()