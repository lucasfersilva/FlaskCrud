from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import login_required,  current_user
from models import Note
from init import db
import json

views = Blueprint('views',__name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method =='POST':
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


