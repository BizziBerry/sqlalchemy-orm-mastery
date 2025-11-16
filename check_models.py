from database import SessionLocal, engine
from models import Author, Book
import sqlalchemy as sa

print('=== ПРОВЕРКА СВЯЗАННЫХ МОДЕЛЕЙ ===')

# Проверяем структуру таблиц
inspector = sa.inspect(engine)

print('1. Структура таблицы authors:')
columns = inspector.get_columns('authors')
for col in columns:
    print(f'   - {col["name"]}: {col["type"]}')

print('2. Структура таблицы books:')  
columns = inspector.get_columns('books')
for col in columns:
    print(f'   - {col["name"]}: {col["type"]}')
    if col['name'] == 'author_id':
        print(f'     VNEShNIJ KLJuCh na authors.id')

print('3. Proverka svjazej:')
session = SessionLocal()
authors = session.query(Author).all()
for author in authors:
    print(f'   Avtor: {author.name} (ID: {author.id})')
    for book in author.books:
        print(f'     Kniga: {book.title} (author_id: {book.author_id})')
session.close()