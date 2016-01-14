from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
#from . forms import NameForm
from ..models import db
from ..models import User, Article, ArticleType, KeyWord, Category, Role


@main.route('/', methods=['GET', 'POST'])
def index():
    glowny = ArticleType.query.filter_by(type_name="book").one()
    author=glowny.articles[0].user.name
    title=glowny.articles[0].title
    body=glowny.articles[0].body
    return render_template('idane.html', author=author, title=title, body=body)

@main.route('/minipodrecznik/<short_title>')
def book_chapter(short_title):
    article = Article.query.filter_by(content_container="minipodrecznik").filter_by(short_title=short_title).one()
    author=article.user.name
    title=article.title
    body=article.body
    return render_template('idane.html', author=author, title=title, body=body)
