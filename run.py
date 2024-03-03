from flask import Flask
from app import create_app
from config  import SECRET_KEY, SQLALCHEMY_DATABASE_URI
import africastalking

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.secret_key = SECRET_KEY



if __name__ == '__main__':
    app.run(debug=True)
