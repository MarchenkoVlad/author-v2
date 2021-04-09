from sqlalchemy.orm import Session
from flask import Blueprint, render_template, abort, request, redirect, url_for
from models import User, Article
from crypt import bcrypt
from forms import AuthForm#, ArticleForm
from sqlalchemy.exc import IntegrityError
import db
import json

wrap = Blueprint('wrap', __name__)


@wrap.route('/')
def get_page():
    return render_template("base.html")


@wrap.route('/index')
def get_page_index():
    return render_template("index.html")


@wrap.route('/signup', methods=['GET', 'POST'])
def signup():
    #получаем данные форм с клиента
    form = AuthForm(request.form)
    print(form.data)
    if request.method == 'POST': #and form.validate():
        user = db.session.query(User).filter_by(email=form.data['email']).first()
        try:
            print('hello')
            new_user = User(first_name=form.data['first_name'], 
                            last_name=form.data['last_name'], 
                            email=form.data['email'],   
                            password=form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return render_template('signup.html', error="Юзер с таким email уже существует")
        return redirect(url_for('wrap.login'))
    return render_template('signup.html')
    

@wrap.route('/login', methods=['POST', 'GET'])
def login():
    form = AuthForm(request.form)
    if request.method == 'POST':
        found_user = db.session.query(User).filter_by(email = form.data['email']).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, form.data['password'])
            if authenticated_user:
                return redirect(url_for('wrap.welcome'))
    return render_template('login.html', form=form)


@wrap.route('/welcome')
def welcome():
    return render_template('welcome.html')


@wrap.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        print(request.form)
        article = Article('авыаваы', 'ыафыаф', 'ffasf')#title=request.form['title'], article_text=request.form['article_text'], intro=request.form['intro'])
        db.session.add(article)
        db.session.commit()
        return redirect('/')

        """try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        
        except:
            return "При добавлении статьи произошла ошибка"
        """
    else:
        return render_template("create_article.html")