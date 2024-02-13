from flask import request, jsonify
from app import app, db
from app.models import Customer, Order
from app.auth import requires_auth

@app.route('/customer', methods=['POST'])
@requires_auth
def create_customer():
    data = request.json
    new_customer = Customer(name=data['name'], code=data['code'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'})

@app.route('/order', methods=['POST'])
@requires_auth
def create_order():
    data = request.json
    customer_id = data['customer_id']
    customer = Customer.query.get(customer_id)
    if customer:
        new_order = Order(item=data['item'], amount=data['amount'], time=data['time'], customer=customer)
        db.session.add(new_order)
        db.session.commit()
        # Send SMS alert to customer here
        return jsonify({'message': 'Order created successfully'})
    else:
        return jsonify({'error': 'Customer not found'})
