from datetime import datetime
from Flask_Projects import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True,nullable=False)
    email=db.Column(db.String(130),unique=True,nullable=False)
    password=db.Column(db.String(30),unique=True,nullable=False)
    img_file=db.Column(db.String(30),nullable=False,default='def.png')
    posts=db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        ser=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=ser.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}','{self.img_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(30),nullable=False)
    date_post=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_post}','{self.content}')"

class ContactUs(db.Model):
    name=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(130),nullable=False)
    phone=db.Column(db.String(30),unique=True,nullable=False,primary_key=True)
    message=db.Column(db.String(300),nullable=False)
    def __repr__(self):
        return f"ContactUs('{self.name}','{self.email}','{self.phone}',{self.message})"
