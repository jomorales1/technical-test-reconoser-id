from flask_security.models import fsqla_v2 as fsqla
from marshmallow import Schema, fields
from src.main import db


class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    pass


class UserSchema(Schema):
    class Meta(Schema.Meta):
        model = User
        sqla_session = db.session

    email = fields.String(required=True)
    password = fields.String(required=True)
