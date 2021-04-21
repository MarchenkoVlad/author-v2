from sqlalchemy.orm import Session
from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from models import User, Article
from crypt import bcrypt
from forms import AuthForm
from sqlalchemy.exc import IntegrityError
import db
import json

wrap = Blueprint('wrap', __name__)


@wrap.route('/')
def get_page():
    return render_template('base.html')


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
        article = Article(title=request.form['title'], article_text=request.form['article_text'], intro=request.form['intro'])
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')

        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create_article.html')


@wrap.route('/posts')
def posts():
    articles = db.session.query(Article).all()
    return render_template('posts.html', articles=articles)


@wrap.route('/posts/<int:article_id>')
def show_article(article_id):  
    article = db.session.query(Article).get(article_id)
    if not article:
        abort(404)
    return render_template('post_detail.html', article=article)


@wrap.route('/posts/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    article = db.session.query(Article).get(article_id)
    try:
        db.session.delete(article)
        db.session.commit()
        return abort(200)
    except:
        return "При удалении статьи возникла ошибка"


@wrap.route('/posts/<int:article_id>/update', methods=['POST', 'GET'])
def update_article(article_id):
    article = db.session.query(Article).get(article_id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.article_text = request.form['article_text']
        try:
            db.session.commit()
            db.session.close()
            return redirect('/posts')
        except:
            return "При изменении статьи произошла ошибка"
    else:
        return render_template("post_update.html", article=article)
