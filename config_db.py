from creds import user_db, password_db, name_db, port
import psycopg2


host = "localhost"

# try:        # Пробуем подключаться к БД
#     connection = psycopg2.connect(
#         host=host
#     )
#     pass
# except Exception as _ex:
#     print("[INFO] Error while working with PostgresSQL", _ex)
# finally:        # Будем закрывать соединение
