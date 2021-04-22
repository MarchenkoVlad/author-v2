from flask import Flask, render_template
from db import engine
from crypt import Bcrypt
from routers import wrap
from flask_login import LoginManager
import db
from models import User

db.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] =True

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "wrap.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(wrap)

if __name__ == '__main__':
    app.run(debug=True)