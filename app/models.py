from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return UserModel.query.filter_by(id=user_id).first()


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


