from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, Relationship, mapped_column
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from helpers import welcome_email
from init import db, bcrypt
from datetime import datetime
from flask import g


DEFAULT_IMG_URL = "https://pngimg.com/d/mandalorian_PNG23.png"
DEFAULT_HEAD_IMG_URL = "https://img.freepik.com/free-photo/glowing-spaceship-orbits-planet-starry-galaxy-generated-by-ai_188544-9655.jpg?w=1480&t=st=1700941711~exp=1700942311~hmac=fe6bbf22f45bbddd98dd7c6e93c48477b10be41e2059b9fb733e7072d76782d9 "


class Follows(db.Model):
    __tablename__ = "follows"

    user_being_followed_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    user_following_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )

    def __init__(self, **kwargs) -> None:
        super(Follows, self).__init__(**kwargs)


class Likes(db.Model):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))

    def __init__(self, **kwargs) -> None:
        super(Likes, self).__init__(**kwargs)


class Notification(db.Model):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(
        String,
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    from_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))


class Repost(db.Model):
    __tablename__ = "reposts"

    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(148), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))

    user = Relationship("User")

    def __init__(self, **kwargs) -> None:
        super(Comment, self).__init__(**kwargs)


class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(148), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    img = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    reposts: Mapped[Repost] = Relationship(
        "Repost", backref="posts", cascade="all,delete-orphan"
    )
    comments: Mapped[Comment] = Relationship(
        "Comment",
        backref="post",
        cascade="all, delete-orphan",
        order_by=("desc(Comment.id)"),
    )

    def __init__(self, **kwargs) -> None:
        super(Post, self).__init__(**kwargs)


# <<<<<<< HEAD
# class Conversation(db.Model):
#     __tablename__ = "conversations"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     content: Mapped[str] = mapped_column(Text)
# =======
class Message(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(148), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    conversation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conversations.id")
    )
    user = Relationship("User")

    def __init__(self, **kwargs) -> None:
        super(Message, self).__init__(**kwargs)


class Conversation(db.Model):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    messages: Mapped[Message] = Relationship(
        "Message", cascade="all, delete-orphan", order_by="desc(Message.id)"
    )
    users = Relationship("User", secondary="messages", backref="conversations")

    def __init__(self, **kwargs) -> None:
        super(Conversation, self).__init__(**kwargs)

    def __repr__(self) -> str:
        if self.sender_id == g.user.id:
            return db.get_or_404(User, self.recipient_id).username
        else:
            return db.get_or_404(User, self.sender_id).username


# class DirectMessage:
#     __tablename__ = "direct_messages"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     timestamp: Mapped[DateTime] = mapped_column(
#         DateTime,
#         nullable=False,
#         default=datetime.utcnow,
#     )
#     conversation_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("conversations.id")
#     )
#     conversation = Relationship("Conversation", backref="messages")


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(
        Text,
        default=DEFAULT_IMG_URL,
    )
    header_image_url: Mapped[str] = mapped_column(
        Text,
        default=DEFAULT_HEAD_IMG_URL,
    )
    bio: Mapped[str] = mapped_column(String(100), default="")
    location: Mapped[str] = mapped_column(String(50), default="")

    posts: Mapped[Post] = Relationship(
        "Post", backref="user", cascade="all, delete-orphan"
    )

    followers: Mapped[Follows] = Relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id),
    )

    following: Mapped[Follows] = Relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id),
    )

    likes: Mapped[Likes] = Relationship(
        "Post",
        secondary="likes",
        backref="users",
        order_by="desc(Likes.id)",
    )

    comments: Mapped[Comment] = Relationship("Comment", cascade="all, delete-orphan")
    commented: Mapped[Post] = Relationship("Post", secondary="comments")
    reposted: Mapped[Repost] = Relationship(
        "Post", secondary="reposts", backref="reposted", cascade="all, delete"
    )

    # direct_messages = Relationship("DirectMessage", secondary="conversations")

    def __init__(self, **kwargs) -> None:
        super(User, self).__init__(**kwargs)

    @classmethod
    def sign_up(cls, email, username, password, image_url, location, bio):
        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf8")
        image_url = image_url if image_url else None
        location = location if location else None
        bio = bio if bio else None
        welcome_email(email, username)

        return cls(
            email=email,
            username=username,
            password=hashed_pwd,
            image_url=image_url,
            location=location,
            bio=bio,
        )

    @classmethod
    def authenticate(cls, username, password):
        """
        authenticate user, first find the username in the database
        then compare the password entered and the user's' password
        if succesful return the user else return False
        """
        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False
