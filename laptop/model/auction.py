from peewee import *

from model.base import Base


class Auction(Base):
    id = AutoField()
    name = CharField()
    price = FloatField(default=0.0)
    img_path = CharField()
    ended = BooleanField(default=False)
    customer = IntegerField(null=True)
