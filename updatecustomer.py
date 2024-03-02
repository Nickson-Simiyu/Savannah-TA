# update_customer_order_ids.py

from app import create_app, db
from app.models import CustomerOrder
from random import randint  # Import this if you need to generate random IDs

def update_order_ids():
    app = create_app()  # Create the Flask application instance
    with app.app_context():  # Create the application context
        # Query and update the existing rows
        orders_with_null_id = CustomerOrder.query.filter_by(id=None).all()
        for order in orders_with_null_id:
            # Generate a unique ID for each order, you can replace this logic as needed
            order.id = randint(1000, 9999)  # Example: generate random 4-digit IDs

        # Commit the changes
        db.session.commit()

if __name__ == "__main__":
    update_order_ids()
