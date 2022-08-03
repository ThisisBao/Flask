from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from .import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods = ["POST","GET"])
@views.route("/home", methods = ["POST","GET"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Quá ngắn!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Thêm ghi chú thành công!", category="success")
    return render_template("home.html", user=current_user)

@views.route("/delete-note", methods = ["POST","GET"])
def delete_note():
    note = json.loads(request.data)
    print(note)
    note_id = note["note_id"]
    result = Note.query.get(note_id)
    if result:
        if result.user_id == current_user.id:
            db.session.delete(result)
            db.session.commit()
    return jsonify({"code": 200})