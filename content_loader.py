#zeby uruchomic zrob:
#exec(open("content_loader.py").read())

from app import db
from app.models import User, Article, ArticleType, KeyWord, Category, Role, ContentContainer
import glob

from time import strptime
from datetime import datetime

db.drop_all()
db.create_all()
piskorski = User(name="Jarosław Piskorski", email="jaropis@zg.home.pl", password="tosiula4221")
db.session.add(piskorski)

minipodrecznik = ContentContainer(title="Minipodręcznik biostatystyki", short_title="minipodrecznik")
paradoksy = ContentContainer(title="Roznosci", short_title="paradoksy")
blog = ContentContainer(title="blog", short_title="Blog")
lista_plikow=glob.glob('content/*.cnt')
for nazwa in lista_plikow:

    plik = open(nazwa, 'r')
    contents = plik.readlines()
    index = 0
    temp = ""

    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    title = temp.strip()
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    short_title = temp.strip()
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    short_body = temp
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    body = temp
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    category = temp.strip()
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + ',' + contents[index]
        index += 1
    keywords = temp.strip()
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    type_name = temp.strip()
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    content_container_title = temp.strip()
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    content_container_short_title = temp.strip()
    if content_container_short_title == "minipodrecznik":
        kontener = minipodrecznik
    if content_container_short_title == "paradoksy":
        kontener = paradoksy
    if content_container_short_title == "blog":
        kontener = blog
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    page_number = temp
    temp = ""

    index += 1
    while contents[index] != "*-*-\n":
        temp = temp + contents[index]
        index += 1
    date_time = strptime(temp.strip(), '%d/%m/%Y')
    date_time = datetime(*date_time[:6]) ## konwerja ze struct_time na datetime, ktore jest przyjmowane przez sqlalchemy
    temp = ""

#    print("tytul:" + title+"krotki tytul: " + short_title + "zawartość: " + body+ "kontener: " + type_name +"numer strony: " + page_number + "content_container"+content_container)

    article = Article(title=title, short_title=short_title, body=body, type_name=ArticleType(type_name=type_name), category=Category(category_name=category), page_number=int(page_number), content_container=kontener, date_time = date_time, short_body=short_body)

    article.user = piskorski

db.session.add(article)
db.session.commit()
