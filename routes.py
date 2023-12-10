from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    url_for,
    session,
    g,
    request,
)
from init import db
from models import Comment, Repost, User, Message
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


#
# @app_routes.before_app_request
# def login():
#     if not g.get("user", None):
#         return redirect(url_for("app_routes.authenticate"))


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

        messages = (
            db.session.execute(
                db.select(Message).order_by(Message.timestamp.desc()).limit(100)
            )
            .scalars()
            .all()
        )

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


@app_routes.route("/logout", methods=["POST"])
def logout():
    do_logout()
    return redirect(url_for("app_routes.authenticate"))


@app_routes.route("/users/<int:user_id>", methods=["GET", "POST"])
def show_user_profile(user_id):
    user = db.get_or_404(User, user_id)
    all_messages_id = db.session.execute(
        db.select(Message.id, Message.timestamp)
        .where(Message.user_id == user_id)
        .union(
            db.select(Message.id, Repost.timestamp)
            .join(Repost)
            .where(Repost.user_id == user_id)
        )
        .order_by(db.desc("timestamp"))
    ).scalars()

    messages = [db.get_or_404(Message, id) for id in all_messages_id]
    form = MessageForm()
    edit_form = EditUserForm(obj=user)
    if form.validate_on_submit():
        message = Message(text=form.text.data, user_id=user.id)
        g.user.messages.append(message)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))
    return render_template(
        "user_profile.html",
        user=user,
        form=form,
        messages=messages,
        edit_form=edit_form,
    )


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
    search = request.args.get("search")
    users = db.session.execute(
        db.select(User).where(User.username.ilike(f"%{search}%")).limit(10)
    ).scalars()
    messages = db.session.execute(
        db.select(Message).where(Message.text.ilike(f"%{search}%")).limit(10)
    ).scalars()
    form = MessageForm()

    return render_template(
        "search.html", users=users, messages=messages, form=form, user=g.user
    )


@app_routes.route("/users/follow", methods=["POST"])
def follow_user():
    if request.json:
        follow_id = request.json["follow_id"]
        user = db.get_or_404(User, follow_id)
        if user in g.user.following:
            print("unfollow")
            g.user.following.remove(user)
        else:
            g.user.following.append(user)
            print("follow")
        db.session.commit()
        return jsonify(response={"response": 200})
    return jsonify(response={"response": "failed"})


@app_routes.route("/users/following/<int:user_id>")
def show_user_following(user_id):
    user = db.get_or_404(User, user_id)
    form = MessageForm()
    edit_form = EditUserForm(obj=user)
    if form.validate_on_submit():
        message = Message(text=form.text.data, user_id=user.id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))

    return render_template(
        "follow_page.html",
        user=user,
        form=form,
        edit_form=edit_form,
        follows=user.following,
    )


@app_routes.route("/users/followers/<int:user_id>")
def show_user_followers(user_id):
    user = db.get_or_404(User, user_id)
    form = MessageForm()
    edit_form = EditUserForm(obj=user)
    if form.validate_on_submit():
        message = Message(text=form.text.data, user_id=user.id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))

    return render_template(
        "follow_page.html",
        user=user,
        form=form,
        edit_form=edit_form,
        follows=user.followers,
    )


@app_routes.route("/messages/", methods=["POST"])
def add_post():
    data = request.json
    print(data)
    form = MessageForm(obj=data)
    if form.validate():
        message = Message()
        form.populate_obj(message)
        g.user.messages.append(message)
        db.session.commit()
        response = {
            "user": {
                "id": g.user.id,
                "username": g.user.username,
                "image_url": g.user.image_url,
            },
            "message": {
                "id": message.id,
                "timestamp": message.timestamp,
                "text": message.text,
            },
        }

        return jsonify(response)
    return jsonify(response={"response": "failed"})


@app_routes.route("/users/messages/likes/<int:user_id>")
def show_liked_messagess(user_id):
    user = db.get_or_404(User, user_id)
    form = MessageForm()
    edit_form = EditUserForm(obj=user)
    if form.validate_on_submit():
        message = Message(text=form.text.data, user_id=user.id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))

    return render_template("likes.html", user=user, form=form, edit_form=edit_form)


@app_routes.route(
    "/messages/<int:message_id>",
)
def show_message(message_id):
    msg = db.get_or_404(Message, message_id)
    comment_form = CommentForm()
    form = MessageForm()
    # if form.validate_on_submit():
    #     comment = Comment()
    #     form.populate_obj(comment)
    #     comment.user_id = g.user.id
    #     comment.message_id = msg.id
    #     msg.comments.append(comment)
    #     db.session.commit()
    #     return redirect(url_for("app_routes.show_message", message_id=msg.id))
    return render_template(
        "message.html", msg=msg, comment_form=comment_form, form=form, user=g.user
    )


@app_routes.route("/messages/comments/add", methods=["POST"])
def add_comment():
    data = request.json
    form = CommentForm(obj=data)
    message = db.get_or_404(Message, request.json["message_id"])
    if form.validate_on_submit():
        comment = Comment()
        form.populate_obj(comment)
        comment.user_id = g.user.id
        comment.message_id = request.json["message_id"]
        db.session.add(comment)
        db.session.commit()
        response = {
            "user": {
                "id": g.user.id,
                "username": g.user.username,
                "image_url": g.user.image_url,
            },
            "comment": {
                "id": comment.id,
                "timestamp": comment.timestamp,
                "text": comment.text,
            },
        }
    return jsonify(response)


@app_routes.route("/messages/comment/delete", methods=["POST"])
def delete_comment():
    if request.json:
        comment_id = request.json["comment_id"]

        comment = db.get_or_404(Comment, comment_id)
        message = db.get_or_404(Message, comment.message_id)

        db.session.delete(comment)
        db.session.commit()
        return jsonify(
            response={
                "response": "deleted",
                "commented": g.user in message.users_commented,
                "message_id": message.id,
            }
        )
    return jsonify(response={"response": "failed"})


@app_routes.route("/messages/delete", methods=["POST"])
def delete_message():
    if request.json:
        message_id = request.json["message_id"]
        msg = db.get_or_404(Message, message_id)
        for comment in msg.comments:
            db.session.delete(comment)
        db.session.delete(msg)
        db.session.commit()
    return jsonify(response={"data": 200})


@app_routes.route("/messages/like/", methods=["POST"])
def like_message():
    if request.json:
        message_id = request.json["message_id"]
        message = db.get_or_404(Message, int(message_id))
        if message in g.user.likes:
            g.user.likes.remove(message)
        else:
            g.user.likes.append(message)
    db.session.commit()
    return jsonify(response={"response": 200})


@app_routes.route("/messages/repost", methods=["POST"])
def respost_message():
    if request.json:
        message_id = request.json["message_id"]
        repost = db.session.execute(
            db.select(Repost).where(
                Repost.message_id == message_id, Repost.user_id == g.user.id
            )
        ).scalar_one_or_none()
        if repost:
            db.session.delete(repost)
        else:
            repost = Repost()
            repost.user_id = g.user.id
            repost.message_id = message_id
            db.session.add(repost)
    db.session.commit()
    return jsonify(response={"response": 200})
