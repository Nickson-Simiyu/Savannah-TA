from flask import jsonify, request
from app import app, db
from app.models import Customer, Order

# Route to add a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], code=data['code'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'})

# Route to add a new order
@app.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    new_order = Order(customer_id=data['customer_id'], item=data['item'], amount=data['amount'], time=data['time'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order added successfully'})
