from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
views = Blueprint('views',__name__)
from .models import Note
from . import db
import json
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
    return render_template("home.html",user=current_user)

@views.route('/home2', methods=['GET','POST'])
@login_required
def home2():
    if request.method == 'POST' or request.method == 'GET':
        return render_template("home2.html",user=current_user)


@views.route('/favorites', methods=['GET','POST'])
@login_required
def favorites():
    if request.method == 'POST' or request.method == 'GET':
        return render_template("favorites.html",user=current_user)

@views.route('/meal_plan', methods=['GET','POST'])
@login_required
def meal_plan():
    if request.method == 'POST' or request.method == 'GET':
        return render_template("meal_plan.html",user=current_user)

@views.route('/discover', methods=['GET','POST'])
@login_required
def discover():
    if request.method == 'POST' or request.method == 'GET':
        return render_template("discover.html",user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})