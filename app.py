from init import create_app, db, bcrypt

app = create_app()
db.init_app(app)
bcrypt.init_app(app)

if __name__ == "__main__":
    app.run()
