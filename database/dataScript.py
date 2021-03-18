#! /usr/bin/env python3
# coding: utf-8

from peewee import *
import mysql.connector


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
    marque = TextField(null = True)
    description = TextField(null = True)
    nutriscore = CharField(1)
    url = TextField(null = True)

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




def my_db_connect():
    mysql_db.connect()

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




def my_db_setter(list_dict):

    ############
    ## peewee ###
    #############

    #mysql_db.connect()
    mysql_db.create_tables([Produit, Categorie, Produit_categorie, Magasin, Produit_magasin])

    for i in list_dict:
        new_product = Produit.create(nom_produit = i['name'],marque = i['brand'], description = i['description'], nutriscore = i['nutriscore'], url = i['url'])
        for element in i['category']:
            new_category, created = Categorie.get_or_create(nom_categorie = element)
            id_product = Produit.select(Produit.unique_id).where(Produit.nom_produit==i['name'])
            id_category = Categorie.select(Categorie.unique_id).where(Categorie.nom_categorie==element)
            res = Produit_categorie.insert(produit_unique_id = id_product, categorie_unique_id = id_category).execute()
        #mettre une boucle pour chaque magasin
        for element in i['store']:
            new_store, created = Magasin.get_or_create(nom_magasin = element)
            id_product = Produit.select(Produit.unique_id).where(Produit.nom_produit==i['name'])
            id_magasin = Magasin.select(Magasin.unique_id).where(Magasin.nom_magasin==element)
            res = Produit_magasin.insert(produit_unique_id = id_product, magasin_unique_id = id_magasin).execute()

def my_db_category_getter():
    query = Categorie.select().order_by(fn.Rand()).limit(15)
    #number_product = Produit.select(fn.count(SQL(('*')))).join(Produit_categorie).where(Produit_categorie.categorie_unique_id == cat.unique_id)
    list_id_cat = []
    for cat in query:
        number_product = Produit.select().join(Produit_categorie).where(Produit_categorie.categorie_unique_id == cat.unique_id)
        print(cat.unique_id, 'la categorie : ', cat.nom_categorie, 'contient', len(number_product), 'produit' )
        list_id_cat.append(cat.unique_id)
    return(list_id_cat)



def my_db_product_getter(id_choice):
    #query = Produit.select().where(Produit.nutriscore == 'A')
    query = Produit.select().join(Produit_categorie).where(Produit_categorie.categorie_unique_id == id_choice)
    for product in query:
        print(product.unique_id, 'produit : ', product.nom_produit, 'nutriscore : ', product.nutriscore)