from flask import Flask
from flask_migrate import Migrate
from blueprints.databases import db
from blueprints.main import main, login_manager
from blueprints.expenses import expense


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.app_context().push()

db.init_app(app)
login_manager.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(main)
app.register_blueprint(expense)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
