from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Настройки базы данных
DB_NAME = 'RecipeDB'
DB_USER = 'postgres'
DB_PASSWORD = '123'
DB_host = 'localhost'
DB_PORT = '5432'


# Установка соединения с базой данных
def connect():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_host,
        port=DB_PORT
    )
    return conn

# Создание таблицы пользователей, если ее нет
def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Добавление пользователя в базу данных
def add_user(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cur.close()
    conn.close()

# Основная страница сайта
@app.route('/')
def index():
    return render_template('index.html')

# Страница входа пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверка наличия пользователя в базе данных
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        print(user)
        cur.close()
        conn.close()
        if user:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# Страница регистрации пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверка наличия пользователя в базе данных
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        if user:
            cur.close()
            conn.close()
            return render_template('register.html', error='Username already exists')
        else:
            cur.close()
            conn.close()
            # Добавление пользователя в базу данных
            add_user(username, password)
            return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)