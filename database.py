# Таблицы и запросы в БД
import sqlite3


# Подключение к базе данных
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()


# Создаем таблицы
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(tg_id INTEGER, name TEXT, number TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, pr_des TEXT, pr_count INTEGER, '
            'pr_price REAL, pr_photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(tg_id INTEGER, user_product TEXT, '
            'user_pr_count INTEGER);')


## Методы пользователя ##
# Регистрация
def register(tg_id, name, num):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);', (tg_id, name, num))
    # Фиксируем изменения
    connection.commit()


# Проверка на наличие пользователя
def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?', (tg_id,)).fetchone():
        return True
    else:
        return False


