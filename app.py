from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from db_init import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///base.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
app.app_context().push()


@app.route('/users')
def get_all_users():
    users_list = [{"id": user.id,
                   "first_name": user.first_name,
                   "last_name": user.last_name,
                   "age": user.age,
                   "email": user.email,
                   "role": user.role,
                   "phone": user.phone}
                  for user in User.query.all()]
    return jsonify(users_list)


@app.route('/users', methods=['POST'])
def post_user():
    data_user = json.loads(request.data)
    user = User(id=data_user['id'],
                first_name=data_user['first_name'],
                last_name=data_user['last_name'],
                age=data_user['age'],
                email=data_user['email'],
                role=data_user['role'],
                phone=data_user['phone'])

    db.session.add(user)
    db.session.commit()
    db.session.close()
    return 'Новый пользователь добавлен'


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if user is None:
        return f'Пользователь id {id} отсутствует'

    db.session.delete(user)
    db.session.commit()
    db.session.close()
    return f'Пользователь id {id} удален'


@app.route('/users/<int:id>', methods=['PUT'])
def put_user(id):
    user = User.query.get(id)

    if user is None:
        return f'Пользователь id {id} отсутствует'

    new_data_user = json.loads(request.data)

    user.first_name = new_data_user['first_name']
    user.last_name = new_data_user['last_name']
    user.age = new_data_user['age']
    user.email = new_data_user['email']
    user.role = new_data_user['role']
    user.phone = new_data_user['phone']

    db.session.add(user)
    db.session.commit()
    db.session.close()
    return f'Данные пользователя id {id} обновлены'


@app.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)

    if user is None:
        return f'Пользователь id {id} отсутсвует'

    return jsonify(
        {"id": user.id,
         "first_name": user.first_name,
         "last_name": user.last_name,
         "age": user.age,
         "email": user.email,
         "role": user.role,
         "phone": user.phone}
    )


@app.route('/orders')
def get_all_orders():
    orders_list = [{"id": _.id,
                    "name": _.name,
                    "description": _.description,
                    "start_date": _.start_date,
                    "end_date": _.end_date,
                    "address": _.address,
                    "price": _.price,
                    "customer_id": _.customer_id,
                    "executor_id": _.executor_id} for _ in Order.query.all()]
    return jsonify(orders_list)


@app.route('/orders', methods=['POST'])
def post_order():
    data_order = json.loads(request.data)

    day_start, month_start, year_start = data_order['start_date'].split("/")
    day_end, month_end, year_end = data_order['end_date'].split("/")

    order = Order(
        id=data_order['id'],
        name=data_order['name'],
        description=data_order['description'],
        start_date=date(year=int(year_start), month=int(month_start), day=int(day_start)),
        end_date=date(year=int(year_end), month=int(month_end), day=int(day_end)),
        address=data_order['address'],
        price=data_order['price'],
        customer_id=data_order['customer_id'],
        executor_id=data_order['executor_id'])

    db.session.add(order)
    db.session.commit()
    db.session.close()
    return 'Новый заказ добавлен'


@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)

    if order is None:
        return f'Заказ id {id} отсутствует'

    db.session.delete(order)
    db.session.commit()
    db.session.close()
    return f'Заказ id {id} удален'


@app.route('/orders/<int:id>', methods=['PUT'])
def put_order(id):
    order = Order.query.get(id)

    if order is None:
        return f'Заказ id {id} отсутствует'

    new_data_order = json.loads(request.data)

    day_start, month_start, year_start = new_data_order['start_date'].split("/")
    day_end, month_end, year_end = new_data_order['end_date'].split("/")

    # Указание стобцов заказа в таблице и новых данных в них
    order.name = new_data_order['name']
    order.description = new_data_order['description']
    order.start_date = date(year=int(year_start), month=int(month_start), day=int(day_start))
    order.end_date = date(year=int(year_end), month=int(month_end), day=int(day_end))
    order.address = new_data_order['address']
    order.price = new_data_order['price']
    order.customer_id = new_data_order['customer_id']
    order.executor_id = new_data_order['executor_id']

    db.session.add(order)
    db.session.commit()
    db.session.close()
    return f'Заказ id {id} обновлен'


@app.route('/orders/<int:id>')
def get_order(id):
    order = Order.query.get(id)

    if order is None:
        return f'Заказ  id {id} отсутствует'

    return jsonify({"id": order.id,
                    "name": order.name,
                    "description": order.description,
                    "start_date": order.start_date,
                    "end_date": order.end_date,
                    "address": order.address,
                    "price": order.price,
                    "customer_id": order.customer_id,
                    "executor_id": order.executor_id})


@app.route('/offers')
def get_all_offers():
    offers_list = [{"id": offer.id,
                    "order_id": offer.order_id,
                    "executor_id": offer.executor_id}
                   for offer in Offer.query.all()]
    return jsonify(offers_list)


@app.route('/offers', methods=['POST'])
def post_offer():
    data_offer = json.loads(request.data)

    offer = Offer(
        id=data_offer['id'],
        order_id=data_offer['order_id'],
        executor_id=data_offer['executor_id'])

    db.session.add(offer)
    db.session.commit()
    db.session.close()
    return 'Новая услуга добавлена'


@app.route('/offers/<int:id>', methods=['DELETE'])
def delete_offer(id):
    offer = Offer.query.get(id)

    if offer is None:
        return f'Услуга id {id} отсутствует'

    db.session.delete(offer)
    db.session.commit()
    db.session.close()
    return f'Услуга id {id} удалена'


@app.route('/offers/<int:id>', methods=['PUT'])
def put_offer(id):
    offer = Offer.query.get(id)

    if offer is None:
        return f'Услуга id {id} отсутствует'

    new_data_offer = json.loads(request.data)

    # Указание стобцов заказа в таблице и новых данных в них
    offer.order_id = new_data_offer['order_id']
    offer.executor_id = new_data_offer['executor_id']

    db.session.add(offer)
    db.session.commit()
    db.session.close()
    return f'Услуга id {id} обновлена'


@app.route('/offers/<int:id>')
def get_offer(id):
    offer = Offer.query.get(id)
    return jsonify({"id": offer.id,
                    "order_id": offer.order_id,
                    "executor_id": offer.executor_id})


if __name__ == '__main__':
    app.run()