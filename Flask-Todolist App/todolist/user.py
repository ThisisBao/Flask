from flask import Blueprint, render_template, request, flash, redirect, url_for
from re import template
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


user = Blueprint("user", __name__)

@user.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Đăng nhập thành công!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Đăng nhập thất bại. Hãy kiểm tra lại!", category="error")
        else:
            flash("Người dùng không tồn tại!", category="error")
    return render_template("login.html", user=current_user)

@user.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Người dùng đã tồn tại!", category="error")
        elif (len(email) < 4):
            flash("Email không hợp lệ!", category="error")
        elif (len(password) < 7):
            flash("Mật khẩu không hợp lệ!", category="error")
        elif password != confirm_password:
            flash("Nhập lại mật khẩu!", category="error")
        else:
            password = generate_password_hash(password, method="sha256")
            new_user = User(email, password, user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Đăng kí thành công!", category="success")
                login_user(user, remember=True)
            except:
                "Lối!!!!!"

    return render_template("signup.html", user=current_user)

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))