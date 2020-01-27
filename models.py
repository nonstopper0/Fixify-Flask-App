# import datetime
# from peewee import *
# from flask_login import UserMixin

DATABASE = PostgresqlDatabase('fixify_app')

class Mechanic(UserMixin, Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    location = CharField()

    class Meta:
        database = DATABASE

class User(Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    cars : [make = CharField(), model = CharField()]

    class Meta:
        database = DATABASE

class Problem(Model):
    make = CharField()
    model = CharField()
    price = CharField()
    problem = CharField()
    id = ForeignKeyField(Mechanic, backref ='problems')
    

    class Meta: 
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Mechanic, Problem], safe=True)
    print('TABLES created')
    DATABASE.close()