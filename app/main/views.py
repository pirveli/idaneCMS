from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
#from . forms import NameForm
from ..models import db
from ..models import User, Article, ArticleType, KeyWord, Category, Role, ContentContainer

# the import below is to sort the instrumentedLists of chapters to create tables of contents
from operator import itemgetter, attrgetter, methodcaller

def generate_chapters_list(content_container_short):
    chapters = Article.query.filter(Article.content_container.has(short_title=content_container_short)).all()
    title = ContentContainer.query.filter_by(short_title=content_container_short).first().title
    chapters=sorted(chapters, key=attrgetter('page_number'))
    titles_list = [(chapter.title, chapter.short_title) for chapter in chapters]
    return(title, titles_list)

def generate_blogs_list(articles, short_body_length):
    def short_body(string, short_body_length):
        letter_number = short_body_length
        while string[letter_number].isalpha():
            letter_number += 1
        return string[:letter_number]

    ## first line
    article = articles[0]
    results=[]
    small_results={}
    small_results['new_row'] = True
    small_results['title'] = article.title
    small_results['short_body'] = article.short_body
    small_results['short_title'] = article.short_title
    small_results['content_container'] = article.content_container
    small_results['short_title'] = article.short_title
    results.append(small_results)

    ## remaining rows
    new_row = True
    for article in articles[1:]:
        small_results = {}
        small_results['new_row'] = new_row
        new_row = not new_row
        small_results['title'] = article.title
        small_results['short_body'] = article.short_body
        small_results['short_title'] = article.short_title
        small_results['content_container'] = article.content_container
        small_results['short_title'] = article.short_title
        
        results.append(small_results)
    return results

@main.route('/', methods=['GET', 'POST'])
def index():
    articles = Article.query.order_by(Article.date_time).all()
    return render_template('index.html', articles=generate_blogs_list(articles, 150))

@main.route('/contents/<content_container_short>')
def table_of_contents(content_container_short):
    articles = Article.query.filter(Article.content_container.has(short_title=content_container_short)).order_by(Article.date_time).all()
    title, titles_list = generate_chapters_list(content_container_short)
    return render_template('table_of_contents.html', articles=generate_blogs_list(articles, 150), titles=titles_list, title=title)

@main.route('/blog', methods=['GET', 'POST'])
def blog_contents():
    articles = Article.query.filter(Article.content_container.has(short_title="blog")).order_by(Article.date_time).all() 
    return render_template('blog.html', articles=generate_blogs_list(articles, 150))

@main.route('/<content_container_short>/<short_title>')
def book_chapter(content_container_short, short_title):
    article = Article.query.filter(Article.content_container.has(short_title = content_container_short)).filter_by(short_title=short_title).one()
    author=article.user.name
    date_time = article.date_time
    chapter_title=article.title
    title, contents = generate_chapters_list(content_container_short)
    body=article.body
    return render_template('book_chapter.html', author=author, title=title, body=body, contents=contents, content_container_short=content_container_short, chapter_title=chapter_title, date_time=date_time)

# @main.route('/contents/<content_container_short>')
# def table_of_contents(content_container_short):
#     title, titles_list = generate_chapters_list(content_container_short)
#     return render_template('table_of_contents.html', titles=titles_list, title=title)

