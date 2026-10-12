from flask import Blueprint,redirect,render_template,request,url_for
from flask_login import current_user,login_user,login_required,logout_user
from project.modules import User
from project.extensions import db
from werkzeug.security import  check_password_hash
auth = Blueprint("auth",__name__)
@auth.route("/login",methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
           return redirect(url_for("main.index"))
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
        if check_password_hash(user.password_hash,password):
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            error = "Invalid email or password. Please try again." 
    return render_template("login.html",error = error)
@auth.route("/register",methods = ["GET","POST"])
def register():

    if current_user.is_authenticated:
       return redirect(url_for("main.index"))
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        pass1 = request.form.get("password")
        pass2 = request.form.get("confirm")
        ck_user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
        if not ck_user:
            if pass1 == pass2:
                user = User(
                    name = name,
                    email = email,
                    password = pass1
                )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("auth.login"))
            else:
                error = "passwords are not similar!"
        else:
            error = "User already exists"

    return render_template("signup.html",error = error)

@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))