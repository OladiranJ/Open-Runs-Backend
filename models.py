# Imports

from peewee         import *
from flask_login    import UserMixin

import datetime


# ------------------------------------------------------------------------------------------------------

# Connecting Database

DATABASE    = SqliteDatabase("parks.sqlite")


# ------------------------------------------------------------------------------------------------------

# Model Setup

class User(UserMixin, Model):
    username    = CharField()
    password    = CharField()
    email       = CharField()
    profpic     = CharField()
    height      = CharField()
    weight      = CharField()
    primary     = CharField()
    secondary   = CharField()
    tertiary    = CharField()
    archtype    = CharField()
    homepark    = CharField()
    parks       = CharField()

    class Meta:
        database    = DATABASE

class Park(Model):
    name    = CharField()
    address = CharField()
    rating  = CharField()
    photo   = CharField()

    class Meta:
        database    = DATABASE


# ------------------------------------------------------------------------------------------------------

# Initialize

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Park], safe = True) 
    print("TABLES CREATED")
    DATABASE.close()