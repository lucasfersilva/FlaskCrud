from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import login_required,  current_user
from models import Note
from init import db
import json
import requests as req

views = Blueprint('views',__name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) <1 :
            flash("note is too short", category ='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota adicionada',category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods =['POST'])
def delete_note():
    note = json.loads(request.data)
    noteid = note['noteId']
    note = Note.query.get(noteid)
    if note:
        db.session.delete(note)
        db.session.commit()
        flash('Nota excluída', category='success')
    else:
        flash('Nota invalida', category='error')

    return render_template("home.html", user=current_user)


@views.route('/get-news', methods=['GET'])
def get_newslist():
    api_key = "DIGITE API THE NEWS API AQUI"
    country = "br"
    lang = "pt"
    url = f"https://api.thenewsapi.com/v1/news/top?api_token={api_key}&locale={country}&limit=5&language={lang}"
    top = req.get(url)
    json_data = top.json()
    news = []
    links = []
    descricao = []
    img_url = []

    for article in json_data['data']:
        title = article['title']
        link = article['url']
        desc = article['description']
        img = article['image_url']
        descricao.append(desc)
        news.append(title)
        links.append(link)
        img_url.append(img)

        print(url)
    zipped_lists = zip(news ,links, descricao, img_url)
    print(news)
    return render_template("news.html", data=zipped_lists,user=current_user)

