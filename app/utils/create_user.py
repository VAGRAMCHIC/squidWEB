import sqlite3
import bcrypt

# Создание/подключение к базе данных
conn = sqlite3.connect('../app.db')
cursor = conn.cursor()

# Создание таблицы (если не существует)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
''')
conn.commit()

def create_user():
    """Функция для создания нового пользователя"""
    print("\nРегистрация нового пользователя")
    username = input("Имя пользователя: ").strip()
    email = input("Email: ").strip()
    password = input("Пароль: ").strip()

    # Проверка уникальности имени и email
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        print("Ошибка: Пользователь с таким именем или email уже существует")
        return False

    # Хеширование пароля с bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Вставка данных в БД
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hashed_password.decode('utf-8'))
        )
        conn.commit()
        print("Пользователь успешно создан!")
        return True
    except sqlite3.IntegrityError:
        print("Ошибка: Не удалось создать пользователя (нарушение уникальности)")
        return False

# Основной цикл программы
if __name__ == "__main__":
    while True:
        create_user()
        if input("\nСоздать еще одного пользователя? (y/n): ").lower() != 'y':
            break

    # Закрытие соединения
    conn.close()
    print("Работа завершена. База данных сохранена в 'users.db'")
