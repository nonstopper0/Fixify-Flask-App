import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.postgres_ext import *

DATABASE = PostgresqlExtDatabase('fixify_app')

class Mechanic(UserMixin, Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    location = CharField()
    specialities = ArrayField(CharField)

    class Meta:
        database = DATABASE

class User(Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    location = CharField()
    cars = ArrayField(CharField)

    class Meta:
        database = DATABASE

class Problem(Model):
    car = CharField()
    price = CharField()
    description = CharField()
    location = CharField()
    owner = ForeignKeyField(User, backref ='problem')
    
    class Meta: 
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Mechanic, Problem], safe=True)
    print('TABLES created')
    DATABASE.close()