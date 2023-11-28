from flask import Blueprint, redirect, render_template, url_for, session, g, request
from init import db
from models import User, Message
from forms import CommentForm, EditUserForm, LoginForm, MessageForm, UserForm

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
        g.user = None


def do_login(id):
    user_id = session.get("user_id", None)
    if not user_id:
        session["user_id"] = id


def do_logout():
    if session.get("user_id", None):
        del session["user_id"]
        g.user = None


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
    return redirect(url_for("app_routes.authenticate"))


@app_routes.route("/authenticate", methods=["GET", "POST"])
def authenticate():
    signup_form = UserForm()
    login_form = LoginForm()

    if signup_form and signup_form.validate_on_submit():
        user = User.sign_up(
            username=signup_form.username.data,
            email=signup_form.email.data,
            password=signup_form.password.data,
            image_url=signup_form.image_url.data,
        )
        db.session.add(user)
        db.session.commit()
        do_login(user.id)
        return redirect(url_for("app_routes.home"))
    elif login_form.validate_on_submit():
        user = User.authenticate(
            username=login_form.username.data, password=login_form.password.data
        )
        if user:
            do_login(user.id)

        return redirect(url_for("app_routes.home"))
    return render_template(
        "authenticate.html", signup_form=signup_form, login_form=login_form
    )


# def login(form):
#                     return redirect(url_for("app_routes.home"))
#
#     return render_template("login.html", form=form)


@app_routes.route("/logout", methods=["POST"])
def logout():
    do_logout()
    return redirect(url_for("app_routes.authenticate"))


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
    user = db.get_or_404(User, user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))

    return render_template("edit_user_profile.html", form=form)


@app_routes.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    do_logout()
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("app_routes.authenticate"))


@app_routes.route("/search")
def search():
    name = request.args.get("search")
    users = db.session.execute(
        db.select(User).where(User.username.ilike(f"%{name}%"))
    ).scalars()
    return render_template("search.html", users=users)


@app_routes.route("/users/follow/<int:follow_id>", methods=["POST"])
def follow_user(follow_id):
    user = db.get_or_404(User, follow_id)
    g.user.followings.append(user)
    db.session.commit()
    return redirect(url_for("app_routes.home"))


@app_routes.route("/users/unfollow/<int:follow_id>", methods=["POST"])
def unfollow_user(follow_id):
    user = db.get_or_404(User, follow_id)
    g.user.followings.remove(user)
    db.session.commit()
    return redirect(url_for("app_routes.home"))


@app_routes.route("/users/followings/<int:user_id>")
def show_user_following(user_id):
    user = db.get_or_404(User, user_id)
    return render_template("followings.html", user=user)


@app_routes.route("/users/followers/<int:user_id>")
def show_user_followers(user_id):
    user = db.get_or_404(User, user_id)
    return render_template("followers.html", user=user)


@app_routes.route("/messages/<int:message_id>")
def show_message(message_id):
    msg = db.get_or_404(Message, message_id)
    form = CommentForm()
    if form.validate_on_submit():
        pass

    return render_template("message.html", msg=msg, form=form)


@app_routes.route("/messages/delete/<int:message_id>", methods=["POST"])
def delete_message(message_id):
    msg = db.get_or_404(Message, message_id)
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for("app_routes.home"))


# @app_routes.route("/comments/new/<int:message_id>", methods=["POST"])
# def add_comment(message_id):
#     message = db.get_or_404(Message, message_id)
#     return redirect(url_for("app_routes.show_message", message_id=message_id))
