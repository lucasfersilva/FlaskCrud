from flask import Blueprint, render_template, request, flash
import requests as req
import json

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
    data = request.form
    print(data)
    return render_template('login.html', boolean=True)


@auth.route('/logout')
def logout():
    return render_template('home.html')


@auth.route('/sign-up', methods =['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        print(firstname)
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(email) < 4 or None:
            flash("Email tem que ser maior que 4 caracteres", category="error")

        elif len(firstname) <2:
            flash("Nome muito curto", category="error")

        elif password1 != password2:
            flash("Suas senhas não coincide", category="error")

        else:
            flash("Conta Criada!", category="success")

    return render_template('sign-up.html')

