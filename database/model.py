#! /usr/bin/env python3
# coding: utf-8

""" the model module contains the different classes for create database
with ORM peewee"""

import peewee
import mysql.connector
from tqdm import tqdm

# peewee

mysql_db = peewee.MySQLDatabase(
    "api_open_test", user="food", password="1234", host="localhost"
)



class BaseModel(peewee.Model):
    class Meta:
        database = mysql_db
        # maybe parentheses instead of brackets in the pewwe doc
        table_settings = ["ENGINE=InnoDB", "DEFAULT CHARSET=utf8"]


class Produit(BaseModel):
    unique_id = peewee.AutoField()
    nom_produit = peewee.CharField(200)
    marque = peewee.TextField(null=True)
    description = peewee.TextField(null=True)
    nutriscore = peewee.CharField(1)
    url = peewee.TextField(null=True)


class Categorie(BaseModel):
    unique_id = peewee.AutoField()
    nom_categorie = peewee.CharField(200)


class Produit_categorie(BaseModel):
    produit_unique_id = peewee.ForeignKeyField(Produit)
    categorie_unique_id = peewee.ForeignKeyField(Categorie)

    class Meta:
        primary_key = peewee.CompositeKey("produit_unique_id", "categorie_unique_id")


class Magasin(BaseModel):
    unique_id = peewee.AutoField()
    nom_magasin = peewee.CharField(100)


class Produit_magasin(BaseModel):
    produit_unique_id = peewee.ForeignKeyField(Produit)
    magasin_unique_id = peewee.ForeignKeyField(Magasin)

    class Meta:
        primary_key = peewee.CompositeKey("produit_unique_id", "magasin_unique_id")


class Favoris(BaseModel):
    unique_id = peewee.AutoField()
    fk_unique_id_produit = peewee.ForeignKeyField(Produit)


class Database_creation:

    def __init__(self):
        self.db_connexion = mysql.connector.connect(
            user="root", password="12345678", host="localhost"
            )

    def my_db_create(self):
    # mysql.connector
    # creating database_cursor to perform SQL operation
        cursor = self.db_connexion.cursor()

    # executing cursor with execute method and pass SQL query
        cursor.execute("CREATE DATABASE IF NOT EXISTS api_open_test")
        cursor.execute("CREATE USER IF NOT EXISTS 'food'@'localhost' IDENTIFIED BY '1234'")
        cursor.execute("""GRANT ALL PRIVILEGES ON api_open_test.* TO 
            'food'@'localhost'""")

    def my_db_setter(self, list_dict):
    # peewee
        mysql_db.create_tables(
            [Produit, Categorie, Produit_categorie, Magasin, Produit_magasin,
                Favoris]
        )

        for i in tqdm(list_dict):
        #tqdm add loading tool progression
            new_product = Produit.create(
                nom_produit=i["name"],
                marque=i["brand"],
                description=i["description"],
                nutriscore=i["nutriscore"],
                url=i["url"],
            )
            for category in i["category"]:
                category = category.strip()
            # strip() remove spaces before and after item
                new_category, created = Categorie.get_or_create(
                    nom_categorie=category)
                id_product = Produit.select(Produit.unique_id).where(
                    Produit.nom_produit == i["name"]
                )
                id_category = Categorie.select(Categorie.unique_id).where(
                    Categorie.nom_categorie == category
                )
                res = Produit_categorie.insert(
                    produit_unique_id=id_product, categorie_unique_id=id_category
                ).execute()
            # make a loop for each store
            for store in i["store"]:
                store = store.strip()
                new_store, created = Magasin.get_or_create(nom_magasin=store)
                id_product = Produit.select(Produit.unique_id).where(
                    Produit.nom_produit == i["name"]
                )
                id_magasin = Magasin.select(Magasin.unique_id).where(
                    Magasin.nom_magasin == store
                )
                res = Produit_magasin.insert(
                    produit_unique_id=id_product, magasin_unique_id=id_magasin
                ).execute()


