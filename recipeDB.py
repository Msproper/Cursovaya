import psycopg2

# Установка соединения с PostgreSQL
conn = psycopg2.connect(database="mydatabase", user="postgres", password="mypassword", host="localhost", port="5432")

# Создание курсора
cur = conn.cursor()

# Создание таблицы
cur.execute("CREATE TABLE mytable (id SERIAL PRIMARY KEY, name VARCHAR(255), age INTEGER)")

conn.commit()

conn.close()