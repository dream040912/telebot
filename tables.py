from peewee import *

db = SqliteDatabase("analiz.db")


class Games(Model):
    DoesNotExist = None
    name_game = CharField(unique=True)
    price_game = FloatField()

    class Meta:
        database = db


Games.create_table()

class Ads(Model):
    title_ad = CharField()
    price_ad = FloatField()

    class Meta:
        database = db

Ads.create_table()

