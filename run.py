from flask import Flask
from app.routes import add_order 
from app import create_app
from config  import SECRET_KEY, SQLALCHEMY_DATABASE_URI
import africastalking

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.secret_key = SECRET_KEY



if __name__ == '__main__':
    africastalking.SMS.send(
    message, 
    [phone_number]
    )
    app.run(debug=True)
