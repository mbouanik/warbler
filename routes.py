from flask import Blueprint, redirect, render_template, url_for, session, g
from init import db
from models import User, Message, Follows, Likes
from forms import EditUserForm, LoginForm, MessageForm, UserForm

app_routes = Blueprint(
    "app_routes",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/app_routes/static",
)


@app_routes.before_request
def add_user_to_g():
    user_id = session.get("user_id", None)
    if user_id:
        g.user = db.get_or_404(User, user_id)
    else:
        g.user = user_id


@app_routes.route("/", methods=["GET", "POST"])
def home():
    user_id = session.get("user_id", None)
    if user_id:
        user = db.get_or_404(User, user_id)
        form = MessageForm()
        messages = db.session.execute(
            db.select(Message).order_by(Message.timestamp.desc()).limit(100)
        ).scalars()

        if form.validate_on_submit():
            message = Message(text=form.text.data, user_id=user.id)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for("app_routes.home"))
        return render_template("home.html", user=user, form=form, messages=messages)
    return redirect(url_for("app_routes.signup"))


@app_routes.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserForm()

    if form and form.validate_on_submit():
        user = User.sign_up(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            image_url=form.image_url.data,
        )
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect(url_for("app_routes.home"))
    return render_template("sign_up.html", form=form)


@app_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data, password=form.password.data
        )
        if user:
            session["user_id"] = user.id
            return redirect(url_for("app_routes.home"))

    return render_template("login.html", form=form)


@app_routes.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    return redirect(url_for("app_routes.login"))


@app_routes.route("/users/<int:user_id>", methods=["GET", "POST"])
def show_user_profile(user_id):
    user = db.get_or_404(User, user_id)
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(text=form.text.data, user_id=user.id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))
    return render_template("user_profile.html", user=user, form=form)


@app_routes.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user_profile(user_id):
    user = db.get_or_404(User, g.user.id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))

    return render_template("edit_user_profile.html", form=form)


@app_routes.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = db.get_or_404(User, g.user.id)
    db.session.delete(user)
    db.session.commit()
    session.pop("user_id")
    return redirect(url_for("app_routes.signup"))
