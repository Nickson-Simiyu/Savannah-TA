from flask import Flask
from app import create_app

app = create_app()

@app.route('/')
def index():
    return "Hello World with flask"


if __name__ == '__main__':
    app.run(debug=True)
