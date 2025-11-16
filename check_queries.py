from sqlalchemy.orm import joinedload
from models import Author, Book
from database import SessionLocal
import sqlalchemy as sa

print('=== SRAVNENIE KOLICHESTVA SQL-ZAPROSOV ===')

engine = sa.create_engine('sqlite:///library.db', echo=False)
Session = sa.orm.sessionmaker(bind=engine)
session = Session()

print('1. LENIVAYA ZAGRUZKA:')
query_count = 0

def count_queries(conn, cursor, statement, parameters, context, executemany):
    global query_count
    query_count += 1
    print(f'   Zapros {query_count}: {statement}')

sa.event.listen(engine, 'before_cursor_execute', count_queries)

authors = session.query(Author).all()
print(f'   Najdeno avtorov: {len(authors)}')
for author in authors:
    books = author.books
    print(f'   Avtor {author.name} imeet {len(books)} knig')

print(f'   VSEGO ZAPROSOV: {query_count}')

query_count = 0
sa.event.remove(engine, 'before_cursor_execute', count_queries)

print('2. ZhADNAYA ZAGRUZKA:')
sa.event.listen(engine, 'before_cursor_execute', count_queries)

authors = session.query(Author).options(joinedload(Author.books)).all()
print(f'   Najdeno avtorov: {len(authors)}')
for author in authors:
    books = author.books
    print(f'   Avtor {author.name} imeet {len(books)} knig')

print(f'   VSEGO ZAPROSOV: {query_count}')

session.close()