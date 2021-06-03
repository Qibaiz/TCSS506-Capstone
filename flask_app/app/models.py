from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return UserModel.query.filter_by(id=user_id).first()


# user_favorites = db.Table('user_favorites',
#                           db.Column('user_id', db.Integer, db.ForeignKey('userModel.id')),
#                           db.Column('county_id', db.Integer, db.ForeignKey('county.id')),
#                           )


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    # favorites = db.relationship('County', secondary=user_favorites, backref=db.backref('trackers', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username


# class County(db.Model, UserMixin):
#     __tablename__ = 'counties'
#
#     id = db.Column(db.Integer, primary_key=True)
#     county_name = db.Column(db.String(80), unique=True, nullable=False)


