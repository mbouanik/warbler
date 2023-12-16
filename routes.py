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
from models import Comment, Repost, User, Message, Likes
from forms import CommentForm, EditUserForm, LoginForm, MessageForm, UserForm
from functools import wraps

app_routes = Blueprint(
    "app_routes",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/app_routes/static",
)


# verify if you login
def is_authenticated():
    return "user_id" in session


# decorator for accessing each page you need to be login
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for("app_routes.authenticate"))
        return view(*args, **kwargs)

    return wrapped_view


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


# home page diplay all messages posted by users if login or home for not login with sign up button
@app_routes.route("/", methods=["GET", "POST"])
# @login_required
def home():
    user_id = session.get("user_id", None)
    if user_id:
        user = db.get_or_404(User, user_id)
        form = MessageForm()

        messages = (
            db.session.execute(
                db.select(Message).order_by(Message.timestamp.desc()).limit(20)
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
    return render_template("home-non.html")

    return redirect(url_for("app_routes.authenticate"))


@app_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data, password=form.password.data
        )
        if user:
            do_login(user.id)

        return redirect(url_for("app_routes.home"))
    return render_template("login.html", form=form)


@app_routes.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = UserForm()

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
    return render_template("signup.html", form=signup_form)


# login or signup
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
    elif login_form and login_form.validate_on_submit():
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
@login_required
def logout():
    do_logout()
    return redirect(url_for("app_routes.authenticate"))


# show profile user
@app_routes.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
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
        .limit(10)
    ).scalars()
    repost_id = [message.id for message in user.reposted]

    messages = [db.get_or_404(Message, id) for id in all_messages_id]
    msgs = []
    for msg in messages:
        if msg.id in repost_id:
            msgs.append(
                {
                    "message": msg,
                    "original": False,
                }
            )
            repost_id.remove(msg.id)
        else:
            msgs.append(
                {
                    "message": msg,
                    "original": True,
                }
            )

    form = MessageForm()
    edit_form = EditUserForm(obj=user)
    if form.validate_on_submit():
        message = Message(text=form.text.data, user_id=user.id)
        g.user.messages.append(message)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=g.user.id))
    return render_template(
        "user_profile.html",
        user=user,
        form=form,
        messages=messages,
        edit_form=edit_form,
        msgs=msgs,
    )


# edit  profile user
@app_routes.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_user_profile(user_id):
    user = db.get_or_404(User, user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))

    return render_template("edit_user_profile.html", form=form)


# delete an user
@app_routes.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    do_logout()
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("app_routes.authenticate"))


# search function for users and messages
@app_routes.route("/search")
@login_required
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


# follow and unfollow users
@app_routes.route("/users/follow", methods=["POST"])
@login_required
def follow_user():
    if request.json:
        follow_id = request.json["follow_id"]
        user = db.get_or_404(User, follow_id)
        if user in g.user.following:
            g.user.following.remove(user)
        else:
            g.user.following.append(user)
        db.session.commit()
        return jsonify(response={"response": 200})
    return jsonify(response={"response": "failed"})


# show the following of an user
@app_routes.route("/users/following/<int:user_id>")
@login_required
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
        "following.html",
        user=user,
        form=form,
        edit_form=edit_form,
    )


# show the this of followers of an user
@app_routes.route("/users/followers/<int:user_id>")
@login_required
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
        "followers.html",
        user=user,
        form=form,
        edit_form=edit_form,
    )


# load homepage messages as you scroll down
@app_routes.route("/load-messages", methods=["GET", "POST"])
def load_more_msg():
    offset = 10
    if request.json:
        index = request.json["index"]
        if index + offset >= len(Message.query.all()):
            offset = len(Message.query.all())
        messages = (
            db.session.execute(
                db.select(Message)
                .order_by(Message.timestamp.desc())
                .slice(index, index + offset)
            )
            .scalars()
            .all()
        )

        all_msg = [
            {
                "id": msg.id,
                "text": msg.text,
                "timestamp": msg.timestamp,
                "user_id": msg.user_id,
                "image_url": msg.user.image_url,
                "username": msg.user.username,
                "commented": msg in g.user.comments,
                "like": msg in g.user.likes,
                "repost": msg in g.user.reposted,
                "cmt_cnt": len(msg.comments),
                "likes_cnt": len(msg.users),
                "repost_cnt": len(msg.reposted),
                "guser": g.user.id,
                "follow": msg.user in g.user.following,
            }
            for msg in messages
        ]
        return jsonify(all_msg)
    return jsonify(response={"ok": 200})


# load profile messages as you scroll down
@app_routes.route("/load-profile-msg", methods=["POST"])
def load_more_profiel_msg():
    offset = 10
    if request.json:
        index = request.json["index"]
        user_id = request.json["id"]
        user = db.get_or_404(User, user_id)
        if index + offset >= len(
            db.session.query(Message).filter_by(user_id=user_id).all()
        ):
            offset = len(db.session.query(Message).filter_by(user_id=user_id).all())
        all_messages_id = db.session.execute(
            db.select(Message.id, Message.timestamp)
            .where(Message.user_id == user_id)
            .union(
                db.select(Message.id, Repost.timestamp)
                .join(Repost)
                .where(Repost.user_id == user_id)
            )
            .order_by(db.desc("timestamp"))
            .slice(index, index + offset)
        ).scalars()
        repost_id = [message.id for message in user.reposted]

        messages = [db.get_or_404(Message, id) for id in all_messages_id]

        # serialize messages
        all_msg = []
        for msg in messages:
            all_msg.append(
                {
                    "id": msg.id,
                    "text": msg.text,
                    "timestamp": msg.timestamp,
                    "user_id": msg.user_id,
                    "image_url": msg.user.image_url,
                    "username": msg.user.username,
                    "commented": msg in g.user.comments,
                    "like": msg in g.user.likes,
                    "repost": msg in g.user.reposted,
                    "cmt_cnt": len(msg.comments),
                    "likes_cnt": len(msg.users),
                    "repost_cnt": len(msg.reposted),
                    "guser": g.user.id,
                    "follow": msg.user in g.user.following,
                    "not_original": msg.id in repost_id,
                    "page": user_id == g.user.id,
                    "page_username": user.username,
                }
            )
            if msg.id in repost_id:
                repost_id.remove(msg.id)

        return jsonify(all_msg)
    return jsonify(response={"ok": 200})


# load mor following as you scroll down
@app_routes.route("/load-following-user", methods=["POST"])
def load_following():
    offset = 10
    if request.json:
        index = request.json["index"]
        user_id = request.json["id"]
        user = db.get_or_404(User, user_id)
        users = user.following[index : index + offset]
        # serialize users
        all_user = [
            {
                "id": user.id,
                "username": user.username,
                "image_url": user.image_url,
                "bio": user.bio,
                "following": len(user.following),
                "followers": len(user.followers),
                "guser": g.user.id,
                "follow_you": g.user in user.following,
            }
            for user in users
        ]
        return jsonify(all_user)
    return jsonify("failed")


# load more follower as you scroll down
@app_routes.route("/load-followers-user", methods=["POST"])
def load_followers():
    offset = 10
    if request.json:
        index = request.json["index"]
        user_id = request.json["id"]
        user = db.get_or_404(User, user_id)
        users = user.followers[index : index + offset]
        all_user = [
            {
                "id": user.id,
                "username": user.username,
                "image_url": user.image_url,
                "bio": user.bio,
                "following": len(user.following),
                "followers": len(user.followers),
                "guser": g.user.id,
                "follow_you": g.user in user.following,
                "following": user in g.user.following,
            }
            for user in users
        ]
        return jsonify(all_user)
    return jsonify("failed")


# load more comments as you sxroll down
@app_routes.route("/load-comments", methods=["POST"])
def load_comments():
    offset = 10
    if request.json:
        index = request.json["index"]
        message_id = request.json["message_id"]
        message = db.get_or_404(Message, message_id)
        comments = message.comments[index : index + offset]
        # serialize comments
        cmts = [
            {
                "id": cmt.id,
                "text": cmt.text,
                "timestamp": cmt.timestamp,
                "user_id": cmt.user_id,
                "image_url": cmt.user.image_url,
                "username": cmt.user.username,
                "guser": g.user.id,
                "follow": cmt.user in g.user.following,
            }
            for cmt in comments
        ]
        return jsonify(cmts)
    return jsonify("failed")


# save the message to the database and return the user and message as json to display it on the dom
@app_routes.route("/messages", methods=["POST"])
@login_required
def add_post():
    data = request.json
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


# diplay the messages liked by the user
@app_routes.route("/users/messages/likes/<int:user_id>")
@login_required
def show_liked_messagess(user_id):
    user = db.get_or_404(User, user_id)

    form = MessageForm()
    edit_form = EditUserForm(obj=user)
    return render_template("likes.html", user=user, form=form, edit_form=edit_form)


# load messages liked by the user as you scroll down
@app_routes.route("/load-likes-msg", methods=["POST"])
def load_likes_msg():
    offset = 10
    if request.json:
        index = request.json["index"]
        user_id = request.json["id"]
        user = db.get_or_404(User, user_id)
        if index + offset >= len(Message.query.all()):
            offset = len(Message.query.all())
        messages = (
            db.session.execute(
                db.select(Message)
                .join(Likes)
                .where(Likes.message_id == Message.id, Likes.user_id == user.id)
                .order_by(Likes.id.desc())
                .slice(index, index + offset)
            )
            .scalars()
            .all()
        )

        # serialize messages
        all_msg = [
            {
                "id": msg.id,
                "text": msg.text,
                "timestamp": msg.timestamp,
                "user_id": msg.user_id,
                "image_url": msg.user.image_url,
                "username": msg.user.username,
                "commented": msg in g.user.comments,
                "like": msg in g.user.likes,
                "repost": msg in g.user.reposted,
                "cmt_cnt": len(msg.comments),
                "likes_cnt": len(msg.users),
                "repost_cnt": len(msg.reposted),
                "guser": g.user.id,
                "follow": msg.user in g.user.following,
            }
            for msg in messages
        ]
        return jsonify(all_msg)
    return jsonify(200)


# display the message and a form to add comments
@app_routes.route("/messages/<int:message_id>")
@login_required
def show_message(message_id):
    msg = db.get_or_404(Message, message_id)
    comment_form = CommentForm()
    form = MessageForm()
    return render_template(
        "message.html", msg=msg, comment_form=comment_form, form=form, user=g.user
    )


# add comment to message and return a json with user and comment serialized
# to display on the DOM
@app_routes.route("/messages/comments/add", methods=["POST"])
@login_required
def add_comment():
    data = request.json
    form = CommentForm(obj=data)
    if request.json:
        message = db.get_or_404(Message, request.json["message_id"])
        if form.validate_on_submit():
            comment = Comment()
            form.populate_obj(comment)
            comment.user_id = g.user.id
            comment.message_id = message.id
            message.comments.append(comment)
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
    return jsonify(response={"failed": "failed to add comment"})


# delete a comment
@app_routes.route("/messages/comment/delete", methods=["POST"])
@login_required
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


# delete a message and the comments associated for the message page
# then return to profile page
@app_routes.route("/messages/delete/<int:msg_id>", methods=["POST"])
@login_required
def delete_show_message(msg_id):
    if msg_id:
        message = db.get_or_404(Message, msg_id)
        for cmt in message.comments:
            db.session.delete(cmt)
        db.session.delete(message)
        db.session.commit()
    return redirect(url_for("app_routes.show_user_profile", user_id=g.user.id))


# delete message on other pages likes, home, profile without reloading the page
@app_routes.route("/messages/delete", methods=["POST"])
@login_required
def delete_message():
    if request.json:
        message_id = request.json["message_id"]
        msg = db.get_or_404(Message, message_id)
        for comment in msg.comments:
            db.session.delete(comment)
        db.session.delete(msg)
        db.session.commit()
    return jsonify(response={"data": 200})


# like and unlike functiond
@app_routes.route("/messages/like", methods=["POST"])
@login_required
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


# repost and unrepost
@app_routes.route("/messages/repost", methods=["POST"])
@login_required
def respost_message():
    if request.json:
        message = db.get_or_404(Message, request.json["message_id"])
        if message in g.user.reposted:
            g.user.reposted.remove(message)
        else:
            g.user.reposted.append(message)
        db.session.commit()
    return jsonify(response={"response": 200})
