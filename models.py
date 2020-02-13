import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = PostgresqlDatabase('medconnect_app')

class Patient(UserMixin, Model):
    name = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    symptoms = CharField()
    specialty = CharField()

    class Meta:
        database = DATABASE

class Provider(Model):
    name = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()
    specialty = CharField()
    diagnoses = ForeignKeyField(Patient, backref = 'providers')


    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Patient, Provider], safe = True)
    print ('Tables Created')
    DATABASE.close()

