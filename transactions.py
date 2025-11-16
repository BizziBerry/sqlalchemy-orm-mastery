from sqlalchemy.exc import SQLAlchemyError
from models import User
from database import SessionLocal

def demonstrate_transactions():
    """Демонстрация работы транзакций"""
    print("=== ZADACHA 2: TRANZAKCII I OTKATY ===")
    
    # Очищаем таблицу перед демонстрацией
    session = SessionLocal()
    session.query(User).delete()
    session.commit()
    session.close()
    
    print("\n1. Sozdaem testovyh polzovatelej...")
    create_test_users()
    
    print("\n2. Demonstriruem uspeshnuyu tranzakciyu:")
    successful_transaction()
    
    print("\n3. Demonstriruem tranzakciyu s oshibkoj i otkatom:")
    transaction_with_rollback()
    
    print("\n4. Proverka dannyh posle otkata:")
    check_users_count()

def create_test_users():
    """Создаем тестовых пользователей"""
    session = SessionLocal()
    
    # Добавляем начальных пользователей
    user1 = User(username="alice", email="alice@example.com")
    user2 = User(username="bob", email="bob@example.com")
    
    session.add_all([user1, user2])
    session.commit()
    session.close()
    print("   Sozdano 2 testovyh polzovatelya")

def successful_transaction():
    """Успешная транзакция"""
    session = SessionLocal()
    
    try:
        print("   Nachalo uspeshnoj tranzakcii...")
        
        user3 = User(username="charlie", email="charlie@example.com")
        user4 = User(username="david", email="david@example.com")
        
        session.add(user3)
        session.add(user4)
        session.commit()
        
        print("   ✅ Tranzakciya uspeshno zavershena")
        print("     Dobavleny: charlie, david")
        
    except SQLAlchemyError as e:
        print(f"   ❌ Oshibka: {e}")
        session.rollback()
    finally:
        session.close()

def transaction_with_rollback():
    """Транзакция с ошибкой и откатом"""
    session = SessionLocal()
    
    try:
        print("   Nachalo tranzakcii s oshibkoj...")
        
        # Добавляем пользователей
        user5 = User(username="eve", email="eve@example.com")
        session.add(user5)
        print("   ✅ Dobavlen eve")
        
        # Пытаемся добавить пользователя с существующим username
        user6 = User(username="alice", email="new_alice@example.com")  # Дубликат!
        session.add(user6)
        print("   ❌ Popytka dobavit alice (dublikat)")
        
        # Коммит должен вызвать ошибку
        session.commit()
        print("   ❌ OSHIBKA: Tranzakciya ne otkatilas!")
        
    except SQLAlchemyError as e:
        print(f"   ✅ Tranzakciya otkatilas pri oshibke!")
        print(f"   Oshibka: {e}")
        session.rollback()
    finally:
        session.close()

def check_users_count():
    """Проверяем количество пользователей после отката"""
    session = SessionLocal()
    
    users = session.query(User).all()
    print(f"   Polzovatelej v baze: {len(users)}")
    
    print("   Spisok polzovatelej:")
    for user in users:
        print(f"     - {user.username} ({user.email})")
    
    session.close()

if __name__ == "__main__":
    demonstrate_transactions()