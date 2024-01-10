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
from sqlalchemy.sql import or_
from werkzeug.wrappers import response

from helpers import time_ago, time_ago_message
from init import db
from models import Comment, Conversation, Repost, User, Post, Likes, Message
from forms import (
    CommentForm,
    MessageForm,
    EditUserForm,
    LoginForm,
    PostForm,
    UserForm,
)
from functools import wraps

app_routes = Blueprint(
    "app_routes",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/app_routes/static",
)


# verify if you are login
def is_authenticated():
    return "user_id" in session


# decorator to access any page you need to be login
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
        form = PostForm()

        posts = (
            db.session.execute(
                db.select(Post).order_by(Post.timestamp.desc()).limit(20)
            )
            .scalars()
            .all()
        )

        if form.validate_on_submit():
            post = Post(text=form.text.data, user_id=user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("app_routes.home"))

        return render_template(
            "home.html", user=user, form=form, posts=posts, time=time_ago
        )
    return render_template("home-non.html")


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
    if session.get("user_id", None):
        return redirect(url_for("app_routes.home"))
    signup_form = UserForm()
    login_form = LoginForm()

    if signup_form and signup_form.validate_on_submit():
        user = User.sign_up(
            username=signup_form.username.data,
            email=signup_form.email.data,
            password=signup_form.password.data,
            image_url=signup_form.image_url.data,
            location=signup_form.location.data,
            bio=signup_form.bio.data,
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
    all_posts_id = db.session.execute(
        db.select(Post.id, Post.timestamp)
        .where(Post.user_id == user_id)
        .union(
            db.select(Post.id, Repost.timestamp)
            .join(Repost)
            .where(Repost.user_id == user_id)
        )
        .order_by(db.desc("timestamp"))
        .limit(10)
    ).scalars()
    repost_id = [post.id for post in user.reposted]

    all_posts = [db.get_or_404(Post, id) for id in all_posts_id]
    posts = []
    for pst in all_posts:
        if pst.id in repost_id:
            posts.append(
                {
                    "post": pst,
                    "original": False,
                }
            )
            repost_id.remove(pst.id)
        else:
            posts.append(
                {
                    "post": pst,
                    "original": True,
                }
            )

    form = PostForm()
    edit_form = EditUserForm(obj=user)
    if form.validate_on_submit():
        post = Post(text=form.text.data, user_id=user.id)
        g.user.posts.append(post)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=g.user.id))
    return render_template(
        "user_profile.html",
        user=user,
        form=form,
        edit_form=edit_form,
        posts=posts,
        time=time_ago,
    )


@app_routes.route("/users/conversations")
@login_required
def conversations():
    form = PostForm()
    conversations = db.session.execute(
        db.select(Conversation).where(
            or_(
                Conversation.recipient_id == g.user.id,
                Conversation.sender_id == g.user.id,
            )
        )
    ).scalars()

    return render_template(
        "conversations.html",
        user=g.user,
        form=form,
        conversations=conversations,
    )


@app_routes.route("/conversations/messages/<int:user_id>", methods=["GET", "POST"])
@login_required
def show_conversation(user_id):
    form = PostForm()
    user = db.get_or_404(User, user_id)
    message_form = MessageForm()
    conversation = db.session.execute(
        db.select(Conversation).where(
            Conversation.sender_id == min(g.user.id, user_id),
            Conversation.recipient_id == max(g.user.id, user_id),
        )
    ).scalar_one_or_none()

    if message_form.validate_on_submit():
        print("MESSAGE RECIEVED")
        if not conversation:
            conversation = Conversation(
                sender_id=min(g.user.id, user_id), recipient_id=max(g.user.id, user_id)
            )
        db.session.add(conversation)
        db.session.commit()

        message = Message(
            text=message_form.text.data,
            user_id=g.user.id,
            conversation_id=conversation.id,
        )
        # conversations.messages.append(message)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("app_routes.show_conversation", user_id=user_id))
    return render_template(
        "messages.html",
        form=form,
        message_form=message_form,
        user=user,
        conversation=conversation,
        time=time_ago_message,
    )


@app_routes.route("/conversations/messages/new", methods=["POST"])
def new_message():
    if request.json:
        message_form = MessageForm(obj=request.json)
        if message_form.validate_on_submit():
            message = Message()
            message_form.populate_obj(message)
            # message.conversation_id = request.json["conversation_id"]
            message.user_id = g.user.id
            conversation = db.get_or_404(Conversation, request.json["conversation_id"])
            conversation.messages.append(message)
            db.session.commit()
            response = {
                "text": message.text,
                "timestamp": time_ago_message(message.timestamp),
            }
            return jsonify(response)
    return jsonify({"failed": "new message_error"})


# @app_routes.route("/conversations/new/<int:user_id>", methods=["GET", "POST"])
# def show_new_conversation(user_id):
#     user = db.get_or_404(User, user_id)
#     conversation = db.session.execute(
#         db.select(Conversation).where(
#             Conversation.sender_id == min(g.user.id, user_id),
#             Conversation.recipient_id == max(g.user.id, user_id),
#         )
#     ).scalar_one_or_none()
#     if conversation:
#         return redirect(
#             url_for("app_routes.show_conversation", conversation_id=conversation.id)
#             )
#     return render_template()


@app_routes.route("/conversations/delete/<int:conversation_id>", methods=["POST"])
def delete_conversation(conversation_id):
    conversation = db.get_or_404(Conversation, conversation_id)
    for message in conversation.messages:
        db.session.delete(message)
    db.session.commit()
    db.session.delete(conversation)
    db.session.commit()
    return redirect(url_for("app_routes.conversations"))


# edit  profile user
@app_routes.route("/users/edit", methods=["GET", "POST"])
@login_required
def edit_user_profile():
    user = db.get_or_404(User, g.user.id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=g.user.id))

    return render_template("edit_user_profile.html", form=form)


# delete an user
@app_routes.route("/users/delete", methods=["POST"])
@login_required
def delete_user():
    user = db.get_or_404(User, g.user.id)
    print(g.user)
    do_logout()
    db.session.delete(user)
    db.session.commit()
    g.user = None
    return redirect(url_for("app_routes.authenticate"))


# search function for users and messages
@app_routes.route("/search")
@login_required
def search():
    search = request.args.get("search")
    users = db.session.execute(
        db.select(User).where(User.username.ilike(f"%{search}%")).limit(10)
    ).scalars()
    posts = db.session.execute(
        db.select(Post).where(Post.text.ilike(f"%{search}%")).limit(10)
    ).scalars()
    form = PostForm()

    return render_template(
        "search.html", users=users, posts=posts, form=form, user=g.user, time=time_ago
    )


@app_routes.route("/search-user", methods=["POST"])
def search_user():
    name = request.json["name"]
    users = db.session.execute(
        db.select(User).where(User.username.ilike(f"%{name}%")).limit(10)
    ).scalars()

    response = [
        {
            "id": user.id,
            "image_url": user.image_url,
            "bio": user.bio,
            "username": user.username,
        }
        for user in users
    ]
    return jsonify(response)


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
    form = PostForm()
    edit_form = EditUserForm(obj=user)
    if form.validate_on_submit():
        post = PostForm(text=form.text.data, user_id=user.id)
        db.session.add(post)
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
    form = PostForm()
    edit_form = EditUserForm(obj=user)
    if form.validate_on_submit():
        post = PostForm(text=form.text.data, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("app_routes.show_user_profile", user_id=user.id))

    return render_template(
        "followers.html",
        user=user,
        form=form,
        edit_form=edit_form,
    )


# load homepage Posts as you scroll down
@app_routes.route("/load-posts", methods=["GET", "POST"])
def load_more_post():
    offset = 10
    if request.json:
        index = request.json["index"]
        if index + offset >= len(Post.query.all()):
            offset = len(Post.query.all()) - 1
        posts = (
            db.session.execute(
                db.select(Post)
                .order_by(Post.timestamp.desc())
                .slice(index, index + offset)
            )
            .scalars()
            .all()
        )

        all_posts = [
            {
                "id": post.id,
                "text": post.text,
                "timestamp": post.timestamp,
                "user_id": post.user_id,
                "image_url": post.user.image_url,
                "username": post.user.username,
                "commented": post in g.user.commented,
                "like": post in g.user.likes,
                "repost": post in g.user.reposted,
                "cmt_cnt": len(post.comments),
                "likes_cnt": len(post.users),
                "repost_cnt": len(post.reposted),
                "guser": g.user.id,
                "follow": post.user in g.user.following,
            }
            for post in posts
        ]
        return jsonify(all_posts)
    return jsonify(response={"failed": 404})


# load profile posts as you scroll down
@app_routes.route("/load-profile-post", methods=["POST"])
def load_more_profiel_msg():
    offset = 10
    if request.json:
        index = request.json["index"]
        user_id = request.json["id"]
        user = db.get_or_404(User, user_id)

        all_posts_id = db.session.execute(
            db.select(Post.id, Post.timestamp)
            .where(Post.user_id == user_id)
            .union(
                db.select(Post.id, Repost.timestamp)
                .join(Repost)
                .where(Repost.user_id == user_id)
            )
            .order_by(db.desc("timestamp"))
            .slice(index, index + offset)
        ).scalars()
        repost_id = [post.id for post in user.reposted]

        posts = [db.get_or_404(Post, id) for id in all_posts_id]

        # serialize posts
        all_posts = []
        for post in posts:
            all_posts.append(
                {
                    "id": post.id,
                    "text": post.text,
                    "timestamp": post.timestamp,
                    "user_id": post.user_id,
                    "image_url": post.user.image_url,
                    "username": post.user.username,
                    "commented": post in g.user.commented,
                    "like": post in g.user.likes,
                    "repost": post in g.user.reposted,
                    "cmt_cnt": len(post.comments),
                    "likes_cnt": len(post.users),
                    "repost_cnt": len(post.reposted),
                    "guser": g.user.id,
                    "follow": post.user in g.user.following,
                    "not_original": post.id in repost_id,
                    "page": user_id == g.user.id,
                    "page_username": user.username,
                }
            )
            if post.id in repost_id:
                repost_id.remove(post.id)

        return jsonify(all_posts)
    return jsonify(response={"failed": 404})


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
        post_id = request.json["post_id"]
        post = db.get_or_404(Post, post_id)
        comments = post.comments[index : index + offset]
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


# save the post to the database and return the user and message as json to display it on the dom
@app_routes.route("/posts", methods=["POST"])
@login_required
def add_post():
    data = request.json
    print(data)
    form = PostForm(obj=data)
    if form.validate():
        post = Post()
        form.populate_obj(post)
        g.user.posts.append(post)
        db.session.commit()
        response = {
            "user": {
                "id": g.user.id,
                "username": g.user.username,
                "image_url": g.user.image_url,
            },
            "post": {
                "id": post.id,
                "timestamp": post.timestamp,
                "text": post.text,
            },
        }

        return jsonify(response)
    return jsonify(response={"response": "failed"})


# diplay the posts liked by the user
@app_routes.route("/users/posts/likes/<int:user_id>")
@login_required
def show_liked_post(user_id):
    user = db.get_or_404(User, user_id)

    form = PostForm()
    edit_form = EditUserForm(obj=user)
    return render_template(
        "likes.html", user=user, form=form, edit_form=edit_form, time=time_ago
    )


# load posts liked by the user as you scroll down
@app_routes.route("/load-likes-post", methods=["POST"])
def load_likes_msg():
    offset = 10
    if request.json:
        index = request.json["index"]
        user_id = request.json["id"]
        user = db.get_or_404(User, user_id)
        if index + offset >= len(Post.query.all()):
            offset = len(Post.query.all())
        posts = (
            db.session.execute(
                db.select(Post)
                .join(Likes)
                .where(Likes.post_id == Post.id, Likes.user_id == user.id)
                .order_by(Likes.id.desc())
                .slice(index, index + offset)
            )
            .scalars()
            .all()
        )

        # serialize posts
        all_posts = [
            {
                "id": post.id,
                "text": post.text,
                "timestamp": post.timestamp,
                "user_id": post.user_id,
                "image_url": post.user.image_url,
                "username": post.user.username,
                "commented": post in g.user.commented,
                "like": post in g.user.likes,
                "repost": post in g.user.reposted,
                "cmt_cnt": len(post.comments),
                "likes_cnt": len(post.users),
                "repost_cnt": len(post.reposted),
                "guser": g.user.id,
                "follow": post.user in g.user.following,
            }
            for post in posts
        ]
        return jsonify(all_posts)
    return jsonify("failed")


# display the post and a form to add comments
@app_routes.route("/posts/<int:post_id>")
@login_required
def show_post(post_id):
    post = db.get_or_404(Post, post_id)
    comment_form = CommentForm()
    form = PostForm()
    return render_template(
        "post.html", post=post, comment_form=comment_form, form=form, user=g.user
    )


# add comment to post and return a json with user and comment serialized
# to display on the DOM
@app_routes.route("/posts/comments/add", methods=["POST"])
@login_required
def add_comment():
    data = request.json
    form = CommentForm(obj=data)
    if request.json:
        post = db.get_or_404(Post, request.json["post_id"])
        if form.validate_on_submit():
            comment = Comment()
            form.populate_obj(comment)
            comment.user_id = g.user.id
            comment.post_id = post.id
            post.comments.append(comment)
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
@app_routes.route("/posts/comment/delete", methods=["POST"])
@login_required
def delete_comment():
    if request.json:
        comment_id = request.json["comment_id"]

        comment = db.get_or_404(Comment, comment_id)
        post = db.get_or_404(Post, comment.post_id)

        db.session.delete(comment)
        db.session.commit()
        return jsonify(
            response={
                "response": "deleted",
                # "commented": g.user in post.users_commented,
                "commented": post in g.user.commented,
                "post_id": post.id,
            }
        )
    return jsonify(response={"response": "failed"})


# delete a post and the comments associated for the post page
# then return to profile page
@app_routes.route("/posts/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_show_post_page(post_id):
    if post_id:
        post = db.get_or_404(Post, post_id)
        # for cmt in post.comments:
        #     db.session.delete(cmt)
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("app_routes.show_user_profile", user_id=g.user.id))


# delete post on other pages likes, home, profile without reloading the page
@app_routes.route("/posts/delete", methods=["POST"])
@login_required
def delete_post():
    if request.json:
        post_id = request.json["post_id"]
        post = db.get_or_404(Post, post_id)
        # for comment in post.comments:
        #     db.session.delete(comment)
        db.session.delete(post)
        db.session.commit()
    return jsonify(response={"data": 200})


# like and unlike functiond
@app_routes.route("/posts/like", methods=["POST"])
@login_required
def like_post():
    if request.json:
        post_id = request.json["post_id"]
        post = db.get_or_404(Post, post_id)
        if post in g.user.likes:
            g.user.likes.remove(post)
        else:
            g.user.likes.append(post)
    db.session.commit()
    return jsonify(response={"response": 200})


# repost and unrepost
@app_routes.route("/posts/repost", methods=["POST"])
@login_required
def respost_post():
    if request.json:
        post = db.get_or_404(Post, request.json["post_id"])
        if post in g.user.reposted:
            g.user.reposted.remove(post)
        else:
            g.user.reposted.append(post)
        db.session.commit()
    return jsonify(response={"response": 200})
