from flask import Flask
from blueprints.databases import db
from blueprints.main import main, login_manager


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.app_context().push()

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(main)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
