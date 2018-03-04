from peewee import *
import datetime

db = SqliteDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class App(BaseModel):
    id = IntegerField(unique=True)
    name = CharField()


class Item(BaseModel):
    app = ForeignKeyField(App)
    name = CharField()
    tag = CharField()


class Skin(BaseModel):
    item = ForeignKeyField(Item)
    name = CharField()


class Price(BaseModel):
    skin = ForeignKeyField(Skin)
    measured = DateTimeField(default=datetime.datetime.now)
    value = FloatField()
    currency = CharField()


def connect():
    db.connect()
    db.create_tables([App, Item, Skin, Price])
