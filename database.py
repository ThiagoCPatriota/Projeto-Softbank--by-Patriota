from peewee import *

db = SqliteDatabase('database_Softbank.db')

class User(Model):
    nome = CharField()
    email = CharField(unique=True)
    senha = FloatField()
    cpf = CharField(unique=True)
    
    class Meta:
        database = db

class Account(Model):
    email = CharField()
    usuario = CharField()
    saldo = FloatField()

    class Meta:
        database = db