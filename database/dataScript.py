#! /usr/bin/env python3
# coding: utf-8

from peewee import *
import mysql.connector, pymysql



#############
## peewee ###
#############


mysql_db = MySQLDatabase('api_open_test', user='food', password='1234',host='localhost')

class BaseModel(Model):
    class Meta:
        database = mysql_db
        #peut être des parentheses à la place des crochet dans la doc pewwe
        table_settings = ['ENGINE=InnoDB', 'DEFAULT CHARSET=utf8']

class Produit(BaseModel):
    unique_id = AutoField()
    nom_produit = CharField(200)
    marque = TextField()
    description = TextField()
    nutriscore = CharField(1)
    url = TextField()

class Categorie(BaseModel):
    unique_id = AutoField()
    nom_categorie = CharField(200)

class Produit_categorie(BaseModel):
    produit_unique_id = ForeignKeyField(Produit)
    categorie_unique_id = ForeignKeyField(Categorie)

    class Meta:
        primary_key = CompositeKey('produit_unique_id', 'categorie_unique_id')

class Magasin(BaseModel):
    unique_id = AutoField()
    nom_magasin = CharField(100)

class Produit_magasin(BaseModel):
    produit_unique_id = ForeignKeyField(Produit)
    magasin_unique_id = ForeignKeyField(Magasin)

    class Meta:
        primary_key = CompositeKey('produit_unique_id', 'magasin_unique_id')






def my_db_create():
    ######################
    ## mysql.connector ###
    ######################
    db_connexion = mysql.connector.connect(user='root', password='12345678',host='localhost')

    # creating database_cursor to perform SQL operation
    cursor = db_connexion.cursor()

    # executing cursor with execute method and pass SQL query
    cursor.execute("CREATE DATABASE api_open_test")
    cursor.execute("CREATE USER 'food'@'localhost' IDENTIFIED BY '1234'")
    cursor.execute("GRANT ALL PRIVILEGES ON api_open_test.* TO 'food'@'localhost'")

    #cursor.execute("DROP DATABASE api_create_test")

    # get list of all databases
    cursor.execute("SHOW DATABASES")

    #print all databases
    for x in cursor:
        print(x)




def my_db_getter(list_dict):

    #############
    ## peewee ###
    #############

    #mysql_db.connect()
    mysql_db.create_tables([Produit, Categorie, Produit_categorie, Magasin, Produit_magasin])

    for i in list_dict:
        new_product = Produit.create(nom_produit = i['name'],marque = i['brand'], description = i['description'], nutriscore = i['nutriscore'], url = i['url'])
        new_category = Categorie.create(nom_categorie = i['category'])
        new_store = Magasin.create(nom_magasin = i['store'])