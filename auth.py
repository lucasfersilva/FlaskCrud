from flask import Blueprint, render_template, request, flash, redirect,url_for
import requests as req
import json
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
from init import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

api_key = "MXwF3W2UtbqkY1dNXLufRKiXTxaBgwtemhg7ZH45"
country = "br"
lang = "pt"


def get_top_news():
    url = f"https://api.thenewsapi.com/v1/news/top?api_token={api_key}&locale={country}&limit=5&language={lang}"
    top = req.get(url)
    json_req = top.json()
    list_titles = []
    list_url = []
    list_description = []
    for i in json_req['data']:
        list_titles.append(i['title'])
        list_url.append(i["url"])
        list_description.append(i["description"])

    print(list_url, " ", list_titles, " ", list_description)
    return list_url, list_description, list_titles


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente', category='error')
        else:
            flash('Email não existe', category='error')

    data = request.form
    print(data)
    return render_template('login.html', boolean=True)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods =['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        print(firstname)
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email = email).first()
        if user:
            flash("This email already exists",category='error')

        elif len(email) < 4 or None:
            flash("Email tem que ser maior que 4 caracteres", category="error")

        elif len(firstname) <2:
            flash("Nome muito curto", category="error")

        elif password1 != password2:
            flash("Suas senhas não coincide", category="error")

        else:
            new_user = User(email=email, first_name=firstname, password= generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Conta Criada!", category="success")

            return redirect(url_for('views.home'))

    return render_template('sign-up.html')

