import unittest
from unittest.mock import patch, MagicMock# Import your Flask app
from .app.models import Customer, Order

class TestAddOrderEndpoint(unittest.TestCase):
    @patch('app.routes.africastalking.SMS')
    @patch('app.routes.Customer')
    @patch('app.routes.db.session.add')
    @patch('app.routes.db.session.commit')
    def test_add_order_success(self, mock_commit, mock_add, mock_customer, mock_sms):
        # Set up mock objects and data
        mock_commit.return_value = None
        mock_add.return_value = None
        mock_customer.query.get.return_value = Customer(id=1, name='Test Customer', phone_number='+254112331571')
        mock_sms.send.return_value = {'SMSMessageData': {'Message': 'Sent successfully'}}

        # Make a POST request to add an order
        with app.test_client() as client:
            response = client.post('/orders', json={'customer_id': 1, 'item': 'Test Item', 'amount': 10, 'time': '2024-02-25T12:00:00'})

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Order added successfully')

        # Verify that the SMS was sent to the customer
        mock_sms.send.assert_called_once_with('Hello Test Customer, your order for Test Item has been successfully placed.', ['+1234567890'])

if __name__ == '__main__':
    unittest.main()
