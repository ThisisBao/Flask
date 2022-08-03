from flask import Flask, redirect, url_for, render_template, request,\
    session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path


app = Flask(__name__)
app.config["SECRET_KEY"] = "abc456"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/hello")
def hello():
    if "user" in session:
        name = session["user"]
        return render_template("index.html", name = name, age = "20",
                               car = ["Vinfast", "Mercedes", "Honda"])
    else:
        return redirect(url_for("login"))

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        name = session["user"]
        if request.method == "POST":
            if not request.form["email"] and request.form["name"]:
                User.query.filter_by(name=name).delete()
                db.session.commit()
                flash("Delete user!")
                return redirect(url_for("logout"))
            else:
                email = request.form["email"]
                session["email"] = email
                found_user = User.query.filter_by(name=name).first()
                found_user.email = email
                db.session.commit()
                flash("Email đã updated!")
        elif "email" in session:
            email = session["email"]
        return render_template("user.html", user = name)
    else:
        flash("Login đi tml!", category="success")
        return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# @app.route("/user/<name>")
# def hello_user(name):
#     return f"<h1>Hello {name}</h1>"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        if user_name:
            session["user"] = user_name
            found_user = User.query.filter_by(name = user_name).first()
            if found_user:
                session["email"] = found_user.email
            else:
                user = User(name=user_name,email="temp@gmail.com")
                db.session.add(user)
                db.session.commit()
            flash("Đã Login!",category="success")
            return redirect(url_for("user", user = user_name))
    if "user" in session:
        name = session["user"]
        flash("Đã Login rồi!", category="success")
        return redirect(url_for("user", user = name))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Đã Logout!", category='success')
    return redirect(url_for("login"))

@app.route("/csstest")
def newhome():
    return render_template("newhome.html")


if __name__ == "__main__":
    if not path.exists("user.db"):
        db.create_all(app = app)
        print("Đã tạo Database")
    app.run(debug=True)