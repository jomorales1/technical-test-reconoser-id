import secrets

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.models import fsqla_v2 as fsqla
from src.api.routes.labels import CountLabels
from src.api.routes.words import CountWords

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = secrets.token_urlsafe()
app.config['SECURITY_PASSWORD_SALT'] = str(secrets.SystemRandom().getrandbits(128))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}

db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)

from src.api.models.users import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

db.create_all()

api = Api(app, prefix='/api')

from src.api.routes.users import Users, Login
api.add_resource(CountLabels, '/label/count')
api.add_resource(CountWords, '/word/count')
api.add_resource(Users, '/user')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)
