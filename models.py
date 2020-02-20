import datetime
from peewee import *
# from flask_login import UserMixin
import os
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = PostgresqlDatabase('medconnnect_app')

class Patient(Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    location = CharField()

    class Meta:
        database = DATABASE

class Provider(Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    specialty = CharField()
    location = CharField()

    class Meta:
        database = DATABASE

class Health(Model):
    symptoms = CharField()
    diagnosis = CharField()
    patient_username = CharField()
    provider_username = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Patient, Provider, Health], safe = True)
    print ('Tables Created')
    DATABASE.close()

