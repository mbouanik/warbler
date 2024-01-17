from unittest import TestCase

from init import create_app, db, bcrypt
from dotenv import load_dotenv
from os import getenv

from models import Post, User
from routes import conversations

load_dotenv()
app = create_app()
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI_TEST")
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()


class TestLandingPage(TestCase):
    def test_home_view_not_login(self):
        with app.test_client() as client:
            res = client.get("/")
            data = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Warp", data)


class TestHomeView(TestCase):
    def setUp(self) -> None:
        with app.app_context():
            user = User(
                username="mandalorian",
                email="mandalorian@mandalorian.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id
            self.user = user
            self.client = app.test_client()
            self.client.post(
                "/login",
                data={"username": "mandalorian", "password": "hello1"},
                follow_redirects=True,
            )

    def tearDown(self):
        self.client.post(f"/users/{self.user_id}/delete")
        with app.app_context():
            db.session.delete(self.user)
            db.session.commit()
            db.session.rollback()

    def test_home_page(self):
        res = self.client.post(
            "/login",
            data={"username": "mandalorian", "password": "hello1"},
            follow_redirects=True,
        )
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("mandalorian", data)

    def test_edit_user(self):
        self.client.post(
            f"/users/edit",
            data={
                "username": "dante",
                "email": self.user.email,
                "image_url": self.user.image_url,
                "header_image_url": self.user.header_image_url,
                "bio": self.user.bio,
                "location": self.user.location,
            },
        )
        res = self.client.get(f"/users/{self.user.id}")
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("dante", data)


class TestPost(TestCase):
    def setUp(self) -> None:
        with app.app_context():
            user = User(
                username="mandalorian",
                email="mandalorian@mandalorian.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )
            db.session.add(user)
            db.session.commit()

            post = Post(user_id=user.id, text="This is the way")
            db.session.add(post)
            db.session.commit()
            self.post = post
            self.post_id = post.id

            self.user_id = user.id
            self.user = user
            self.client = app.test_client()
            self.client.post(
                "/login",
                data={"username": "mandalorian", "password": "hello1"},
                follow_redirects=True,
            )

    def tearDown(self):
        with app.app_context():
            db.session.delete(self.post)
            db.session.delete(self.user)
            db.session.commit()
            db.session.rollback()

    def test_delete_msg(self):
        home_page = self.client.get(f"/users/{self.user_id}")
        data = home_page.get_data(as_text=True)
        self.assertEqual(home_page.status_code, 200)
        self.assertIn("This is the way", data)

        self.client.post("/posts/delete", json={"post_id": self.post_id})
        home_page = self.client.get(f"/users/{self.user_id}")
        data = home_page.get_data(as_text=True)

    def test_post(self):
        self.client.post(
            "/posts", json={"text": "For Mandalore"}, follow_redirects=True
        )
        home_page = self.client.get(f"/users/{self.user_id}")
        data = home_page.get_data(as_text=True)
        self.assertEqual(home_page.status_code, 200)
        self.assertIn("For Mandalore", data)


class TestLikes(TestCase):
    def setUp(self) -> None:
        with app.app_context():
            user = User(
                username="mandalorian",
                email="mandalorian@mandalorian.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )
            db.session.add(user)
            db.session.commit()

            post = Post(user_id=user.id, text="This is the way")
            db.session.add(post)
            db.session.commit()

            self.post = post
            self.post_id = post.id
            self.user_id = user.id
            self.user = user
            self.client = app.test_client()
            self.client.post(
                "/login",
                data={"username": "mandalorian", "password": "hello1"},
                follow_redirects=True,
            )

    def tearDown(self):
        with app.app_context():
            db.session.delete(self.user)
            db.session.commit()
            db.session.rollback()

    def test_like(self):
        like = self.client.post("/posts/like", json={"post_id": self.post_id})
        home_page = self.client.get(f"/users/{self.user_id}")
        data = home_page.get_data(as_text=True)
        self.assertEqual(like.status_code, 200)
        self.assertIn('<small id="likes_count"> 1 </small>', data)


class TestRepost(TestCase):
    def setUp(self) -> None:
        with app.app_context():
            user = User(
                username="mandalorian",
                email="mandalorian@mandalorian.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )
            db.session.add(user)
            db.session.commit()

            post = Post(user_id=user.id, text="This is the way")
            db.session.add(post)
            db.session.commit()

            self.user_id = user.id
            self.user = user
            self.post = post
            self.post_id = post.id
            self.client = app.test_client()
            self.client.post(
                "/login",
                data={"username": "mandalorian", "password": "hello1"},
                follow_redirects=True,
            )

    def tearDown(self):
        with app.app_context():
            db.session.delete(self.user)
            db.session.commit()
            db.session.rollback()

    def test_repost(self):
        repost = self.client.post("/posts/repost", json={"post_id": self.post_id})
        home_page = self.client.get(f"/users/{self.user_id}")
        data = home_page.get_data(as_text=True)
        self.assertEqual(repost.status_code, 200)
        self.assertIn(
            """<small id="repost_count"> 1 </small>""",
            data,
        )


class TestComment(TestCase):
    def setUp(self) -> None:
        with app.app_context():
            user = User(
                username="mandalorian",
                email="mandalorian@mandalorian.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )
            db.session.add(user)
            db.session.commit()

            post = Post(user_id=user.id, text="This is the way")
            db.session.add(post)
            db.session.commit()

            self.post = post
            self.post_id = post.id
            self.user_id = user.id
            self.user = user
            self.client = app.test_client()
            self.client.post(
                "/login",
                data={"username": "mandalorian", "password": "hello1"},
                follow_redirects=True,
            )

    def tearDown(self):
        with app.app_context():
            db.session.delete(self.user)
            db.session.commit()
            db.session.rollback()

    def test_comment(self):
        cmt = self.client.post(
            "/posts/comments/add",
            json={"text": "oh nice", "post_id": self.post_id},
        )
        home_page = self.client.get(f"/posts/{self.post_id}")

        data = home_page.get_data(as_text=True)
        self.assertEqual(home_page.status_code, 200)
        self.assertIn(
            "oh nice",
            data,
        )
        self.client.post(
            "/posts/comment/delete", json={"comment_id": cmt.json["comment"]["id"]}
        )
        post = self.client.get(f"posts/{self.post_id}")
        post_page = post.get_data(as_text=True)
        self.assertEqual(post.status_code, 200)
        self.assertNotIn("oh nice", post_page)


class TestFollow(TestCase):
    def setUp(self) -> None:
        with app.app_context():
            user = User(
                username="mandalorian",
                email="mandalorian@mandalorian.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )
            user2 = User(
                username="mace",
                email="mace@mace.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )

            db.session.add_all([user, user2])
            db.session.commit()
            self.client = app.test_client()
            self.user = user
            self.test_user = user2
            self.test_user_id = user2.id

            self.client.post(
                "/login",
                data={"username": "mandalorian", "password": "hello1"},
            )

    def tearDown(self) -> None:
        with app.app_context():
            self.client.post("/logout")
            db.session.delete(self.user)
            db.session.delete(self.test_user)
            db.session.commit()

    def test_following(self):
        self.client.post("/users/follow", json={"follow_id": self.test_user.id})
        following_page = self.client.get(f"/users/following/{self.user.id}")
        data_following = following_page.get_data(as_text=True)

        self.assertEqual(following_page.status_code, 200)
        self.assertIn("mace", data_following)

    def test_followers(self):
        self.client.post("/users/follow", json={"follow_id": self.test_user.id})
        followers_page = self.client.get(f"/users/followers/{self.test_user.id}")
        data_followers = followers_page.get_data(as_text=True)

        self.assertEqual(followers_page.status_code, 200)
        self.assertIn("mandalorian", data_followers)


class TestMessage(TestCase):
    def setUp(self) -> None:
        with app.app_context():
            user = User(
                username="mandalorian",
                email="mandalorian@mandalorian.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )
            user2 = User(
                username="mace",
                email="mace@mace.com",
                password=bcrypt.generate_password_hash("hello1").decode("utf-8"),
            )

            db.session.add_all([user, user2])
            db.session.commit()
            self.client = app.test_client()
            self.user = user
            self.test_user = user2
            self.test_user_id = user2.id

            self.client.post(
                "/login",
                data={"username": "mandalorian", "password": "hello1"},
            )

    def tearDown(self) -> None:
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.rollback()

    def test_send_message(self):
        res = self.client.post(
            "/conversations/messages/new",
            json={"user_id": self.test_user_id, "text": "hello"},
        )

        self.assertEqual(res.status_code, 200)
        messages = self.client.get(f"/conversations/messages/{self.test_user_id}")
        data = messages.get_data(as_text=True)
        self.assertEqual(messages.status_code, 200)
        self.assertIn("hello", data)
        conversation = self.client.get("/users/conversations")
        data = conversation.get_data(as_text=True)

        self.assertEqual(conversation.status_code, 200)
        self.assertIn("mace", data)
