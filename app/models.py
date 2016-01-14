from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db
from . import login_manager

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(usr_id):
    return User.query.get(int(usr_id))

## many to many association table between keyword  and article
association_table = db.Table('association', db.Model.metadata,
                          db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
                          db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id'))
                          )

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
                        
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(80))
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s', email='%s')>" % (
            self.name, self.fullname, self.password, self.email
            )

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True
    
class Article(db.Model):
    __tablename__='articles'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    short_title = db.Column(db.String(20), nullable=False) ## this is just for dynamically creating paths - I want to keep this compatible with the present version of idane.pl
    body = db.Column(db.String(100000), nullable=False)
    short_body = db.Column(db.String(1000), nullable=False)
    content_container_id = db.Column(db.Integer, db.ForeignKey('content_containters.id'))
    content_container = db.relationship('ContentContainer', backref='articles')
    page_number = db.Column(db.Integer()) ## nr. rozdzialu w ksiazce
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='articles')
    ## many-to-many with KeyWord
    keywords = db.relationship('KeyWord', secondary=association_table, backref='articles')
    # one-to-many with Category (is one)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='articles')
    type_id = db.Column(db.Integer, db.ForeignKey('article_types.id'))
    type_name = db.relationship('ArticleType', backref='articles')

    date_time = db.Column(db.DateTime, default=db.func.now())
    def __repr__(self):
        return "<Article(name='%s', user='%s', category='%s')>" % (
            self.name, self.user.name, self.category
            )

class KeyWord(db.Model):
    __tablename__ = 'keywords'
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    keyword = db.Column(db.String(80), nullable=False)

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    category_name = db.Column(db.String(80), nullable = False)

class ArticleType(db.Model):
    __tablename__ = 'article_types'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    type_name = db.Column(db.String(80), nullable = False)

class ContentContainer(db.Model):
    __tablename__ = 'content_containters'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(80), nullable = False)
    short_title = db.Column(db.String(80), nullable = False)
    introduction = db.Column(db.String(100000))
