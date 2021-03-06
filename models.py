import datetime
from peewee import *
import os
from playhouse.db_url import connect

# Replace your DATABASE definition with this block
if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = PostgresqlDatabase('fixify_app')


class Mechanic(Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    location = CharField()
    specialities = CharField()

    class Meta:
        database = DATABASE

class User(Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    location = CharField()

    class Meta:
        database = DATABASE

class Problem(Model):
    car = CharField()
    price = CharField()
    title = CharField()
    description = CharField()
    location = CharField()
    owner_username = CharField()
    mechanic_username = CharField()
    
    class Meta: 
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Mechanic, Problem], safe=True)
    print('TABLES created')
    DATABASE.close()

