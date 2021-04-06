from flask import Flask, render_template
from db import engine
from crypt import Bcrypt
from routers import wrap
import db

db.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] =True

app.register_blueprint(wrap)

if __name__ == '__main__':
    app.run(debug=True)