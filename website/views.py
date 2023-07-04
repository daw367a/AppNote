from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Pobranie notatki z formularza HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            note_id = request.form.get('note_id')  # Pobranie identyfikatora notatki z formularza HTML
            if note_id:  # Jeśli istnieje identyfikator, oznacza to, że notatka ma być zaktualizowana
                existing_note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
                if existing_note:
                    existing_note.data = note  # Aktualizacja treści notatki
                    flash('Note updated!', category='success')
                else:
                    flash('Note not found!', category='error')
            else:  # W przeciwnym razie utworzenie nowej notatki
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                flash('Note added!', category='success')

            db.session.commit()

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # Ta funkcja oczekuje na dane JSON z pliku INDEX.js
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
