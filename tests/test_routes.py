import pytest
import json
from app import app, db
from app.models import Customer, Order

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_create_customer(client):
    response = client.post('/customer', json={'name': 'John Doe', 'code': 'JD001'})
    assert response.status_code == 200
    assert Customer.query.count() == 1

def test_create_order(client):
    client.post('/customer', json={'name': 'John Doe', 'code': 'JD001'})
    customer = Customer.query.first()
    response = client.post('/order', json={'item': 'Laptop', 'amount': 1000.0, 'time': '2024-02-12 12:00:00', 'customer_id': customer.id})
    assert response.status_code == 200
    assert Order.query.count() == 1
