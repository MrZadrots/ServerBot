from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug =True
app.config['SECRET_KEY']  = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:EGORletov2312@localhost/my_db'
db = SQLAlchemy()
@app.route('/')
def index():
    return ("Hello world!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
