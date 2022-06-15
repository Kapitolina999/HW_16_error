from datetime import date
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from models import User, Order, Offer
import data

#Удаление и создание моделей
db.drop_all()
db.create_all()

#Создание объектов для добавления в БД
users = [User(
    id=user['id'],
    first_name=user['first_name'],
    last_name=user['last_name'],
    age=user['age'],
    email=user['email'],
    role=user['role'],
    phone=user['phone'])
    for user in data.users]

orders = []
for order in data.orders:
    month_start, day_start, year_start = order['start_date'].split("/")
    month_end, day_end, year_end = order['end_date'].split("/")
    orders.append(Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=date(year=int(year_start), month=int(month_start), day=int(day_start)),
        end_date=date(year=int(year_end), month=int(month_end), day=int(day_end)),
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']))

offers = [Offer(
    id=offer['id'],
    order_id=offer['order_id'],
    executor_id=offer['executor_id'])
    for offer in data.offers]

#Добавление объектов в сессию
db.session.add_all(users)
db.session.add_all(offers)
db.session.add_all(orders)

#Фиксация изменений в БД
db.session.commit()
