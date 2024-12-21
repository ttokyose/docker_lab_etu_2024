from flask import Flask, render_template, redirect, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
import logging

# Инициализация приложения и базы данных
app = Flask(__name__)

# Настройки для базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/tododb'  # Настроено для PostgreSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений для экономии ресурсов

# Инициализация базы данных и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель Todo
class Todo(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.title} - {self.desc}"

# Главная страница

# Настройка логов
logging.basicConfig(level=logging.INFO)


# Главная страница
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        logging.info("POST request received")
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

        logging.info(f"Task added: {todo}")
        # Перенаправление на тот же маршрут с методом GET после добавления
        return redirect('/')

    logging.info("GET request received")
    alltodo = Todo.query.all()  # Получаем все задачи из базы данных
    return render_template('index.html', alltodo=alltodo)

# Удаление задачи
@app.route('/delete/<int:sr_no>')
def delete(sr_no):
    todo = Todo.query.filter_by(sr_no=sr_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Обновление задачи
@app.route('/update/<int:sr_no>', methods=['GET', 'POST'])
def update(sr_no):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sr_no=sr_no).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sr_no=sr_no).first()
    return render_template('update.html', todo=todo)

# Инициализация базы данных (выполняется только при первом запуске)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создаем все таблицы в базе данных

    app.run(debug=True)