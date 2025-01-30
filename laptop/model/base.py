from peewee import *

db = SqliteDatabase('database/auction.db')


class Base(db.Model):
    class Meta:
        database = db


def init_db():
    db.connect()
    db.create_tables([m for m in Base.__subclasses__()])
