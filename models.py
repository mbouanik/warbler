from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, Relationship, mapped_column
from init import db, bcrypt
from datetime import datetime


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


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(
        Text,
        default="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5024af8d-d5bc-49d0-a1b7-25c50838f6d9/df0oao0-ea61c72c-21d3-4248-95bf-35faa261dfbd.jpg/v1/fit/w_828,h_1104,q_70,strp/battle_droid_commander_by_riccardofasoli_df0oao0-414w-2x.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTcwNyIsInBhdGgiOiJcL2ZcLzUwMjRhZjhkLWQ1YmMtNDlkMC1hMWI3LTI1YzUwODM4ZjZkOVwvZGYwb2FvMC1lYTYxYzcyYy0yMWQzLTQyNDgtOTViZi0zNWZhYTI2MWRmYmQuanBnIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.KELWv9slPr-oEQ9xHoTfDhFi-Fb_T0q5HOSa7C9M_s0",
    )
    header_image_url: Mapped[str] = mapped_column(
        Text,
        default="https://img.freepik.com/free-photo/glowing-spaceship-orbits-planet-starry-galaxy-generated-by-ai_188544-9655.jpg?w=1480&t=st=1700941711~exp=1700942311~hmac=fe6bbf22f45bbddd98dd7c6e93c48477b10be41e2059b9fb733e7072d76782d9",
    )
    bio: Mapped[str] = mapped_column(Text, default="")
    location: Mapped[str] = mapped_column(String, default="")

    messages = Relationship("Message", backref="user", cascade="all, delete")

    followers = Relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id),
        backref="following",
    )

    # following = Relationship(
    #     "User",
    #     secondary="follows",
    #     primaryjoin=(Follows.user_following_id == id),
    #     secondaryjoin=(Follows.user_being_followed == id),
    # )

    likes = Relationship("Message", secondary="likes", backref="users")

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


class Message(db.Model):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(140), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow()
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    comments = Relationship("Comment", backref="message")

    def __init__(self, **kwargs) -> None:
        super(Message, self).__init__(**kwargs)


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(140), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow()
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id"))

    user = Relationship("User")

    def __init__(self, **kwargs) -> None:
        super(Comment, self).__init__(**kwargs)
