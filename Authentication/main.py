from flask import Flask, render_template, redirect, request
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel, login, db

app = Flask(__name__)

app.config["SECRET_KEY"] = "XafGH12Cxhij231GB"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login.init_app(app)

login.login_view = "login"


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/blogs")
@login_required
def blogs():
    return render_template("blog.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/blogs")

    if request.method == "POST":
        email = request.form["email"]
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form["password"]):
            login_user(user)
            return redirect("/blogs")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/blogs")

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        if UserModel.query.filter_by(email=email).first():
            return "Email already exist !"

        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/blogs")


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
