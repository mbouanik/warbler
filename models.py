from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, Relationship, mapped_column
from init import db, bcrypt
from datetime import datetime

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
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id"))

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

    message_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("messages.id"), primary_key=True
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
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id"))

    user = Relationship("User")

    def __init__(self, **kwargs) -> None:
        super(Comment, self).__init__(**kwargs)


class Message(db.Model):
    __tablename__ = "messages"
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
        "Repost", backref="messages", cascade="all,delete-orphan"
    )
    comments: Mapped[Comment] = Relationship(
        "Comment",
        backref="message",
        cascade="all, delete-orphan",
        order_by=("desc(Comment.id)"),
    )
    users_commented = Relationship("User", secondary="comments")

    def __init__(self, **kwargs) -> None:
        super(Message, self).__init__(**kwargs)


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

    messages: Mapped[Message] = Relationship(
        "Message", backref="user", cascade="all, delete-orphan"
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
        "Message",
        secondary="likes",
        backref="users",
        order_by="desc(Likes.id)",
    )

    comments: Mapped[Comment] = Relationship(
        "Message", secondary="comments", cascade="all, delete"
    )
    reposted: Mapped[Repost] = Relationship(
        "Message", secondary="reposts", backref="reposted", cascade="all, delete"
    )

    def __init__(self, **kwargs) -> None:
        super(User, self).__init__(**kwargs)

    @classmethod
    def sign_up(cls, email, username, password, image_url):
        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf8")
        image_url = image_url if image_url else None

        return cls(
            email=email, username=username, password=hashed_pwd, image_url=image_url
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
