#! /usr/bin/env python3
# coding: utf-8

""" the dataScript module contains the different classes for create database
and functions to manage the database"""

import peewee
import mysql.connector
from tqdm import tqdm

#############
## peewee ###
#############


mysql_db = peewee.MySQLDatabase(
    "api_open_test", user="food", password="1234", host="localhost"
)


class BaseModel(peewee.Model):
    class Meta:
        database = mysql_db
        # peut être des parentheses à la place des crochet dans la doc pewwe
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


def my_db_connect():
    mysql_db.connect()


def my_db_create():
    ######################
    ## mysql.connector ###
    ######################
    db_connexion = mysql.connector.connect(
        user="root", password="12345678", host="localhost"
    )

    # creating database_cursor to perform SQL operation
    cursor = db_connexion.cursor()

    # executing cursor with execute method and pass SQL query
    cursor.execute("CREATE DATABASE api_open_test")
    cursor.execute("CREATE USER 'food'@'localhost' IDENTIFIED BY '1234'")
    cursor.execute("""GRANT ALL PRIVILEGES ON api_open_test.* TO 
        'food'@'localhost'""")

    # cursor.execute("DROP DATABASE api_create_test")

    # get list of all databases
    # cursor.execute("SHOW DATABASES")

    # print all databases
    # for x in cursor:
    #    print(x)


def my_db_setter(list_dict):

    ############
    ## peewee ###
    #############

    # mysql_db.connect()
    mysql_db.create_tables(
        [Produit, Categorie, Produit_categorie, Magasin, Produit_magasin,
            Favoris]
    )

    for i in tqdm(list_dict):
        new_product = Produit.create(
            nom_produit=i["name"],
            marque=i["brand"],
            description=i["description"],
            nutriscore=i["nutriscore"],
            url=i["url"],
        )
        for category in i["category"]:
            category = category.strip()
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
        # mettre une boucle pour chaque magasin
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


def my_db_category_getter():
    query = Categorie.select().order_by(peewee.fn.Rand()).limit(15)
    list_id_cat = []
    for cat in query:
        number_product = (
            Produit.select()
            .join(Produit_categorie)
            .where(Produit_categorie.categorie_unique_id == cat.unique_id)
        )
        print(
            cat.unique_id,
            "la categorie : ",
            cat.nom_categorie,
            "contient",
            len(number_product),
            "produit",
        )
        list_id_cat.append(cat.unique_id)
    return list_id_cat


def my_db_product_getter(id_choice):
    # query = Produit.select().where(Produit.nutriscore == 'A')
    query = (
        Produit.select()
        .join(Produit_categorie)
        .where(Produit_categorie.categorie_unique_id == id_choice)
    )
    list_id_prod = []
    for product in query:
        print(
            product.unique_id,
            "produit : ",
            product.nom_produit,
            "nutriscore : ",
            product.nutriscore,
        )
        list_id_prod.append(product.unique_id)
    return list_id_prod


def my_db_product_name_getter(id_prod):
    query = Produit.select().where(Produit.unique_id == id_prod)
    product_name = []
    for product in query:
        product_name.append(product.nom_produit)
    return product_name[0]


def my_db_substitute_getter(id_choice):

    list_substitute = {}
    query_cat = (
        Categorie.select()
        .join(Produit_categorie)
        .where(Produit_categorie.produit_unique_id == id_choice)
    )
    for category in query_cat:
        query_substitute = (
            Produit.select()
            .join(Produit_categorie)
            .where(
                Produit_categorie.categorie_unique_id == category.unique_id)
        )
        for product in query_substitute:
            if product.unique_id in list_substitute.keys():
                list_substitute[product.unique_id] += 1
            else:
                list_substitute[product.unique_id] = 1
    sorted_dict = sorted(list_substitute.items(
        ), key=lambda t: t[1], reverse=True)
    i = 1
    query = Produit.select().where(Produit.unique_id == id_choice)
    query_nutriscore = ""
    query_best_id = 0
    query_same_id = 0
    query_best_nutriscore = ""
    query_same_nutriscore = ""
    for product in query:
        query_nutriscore = product.nutriscore

    while not query_best_nutriscore and not query_same_nutriscore:
        while i < len(sorted_dict) and not query_best_nutriscore:
            query_best = Produit.select().where(
                Produit.unique_id == sorted_dict[i][0])
            for product in query_best:
                query_best_nutr_temp = product.nutriscore
                query_best_id_temp = product.unique_id
            if query_best_nutr_temp < query_nutriscore:
                query_best_nutriscore = query_best_nutr_temp
                query_best_id = query_best_id_temp
            else:
                i += 1
        if not query_best_nutriscore:
            i = 1
            while i < len(sorted_dict) and not query_same_nutriscore:
                query_best = Produit.select().where(
                    Produit.unique_id == sorted_dict[i][0]
                )
                for product in query_best:
                    query_same_nutr_temp = product.nutriscore
                    query_same_id_temp = product.unique_id
                if query_same_nutr_temp == query_nutriscore:
                    query_same_nutriscore = query_same_nutr_temp
                    query_best_id = query_same_id_temp
                else:
                    i += 1

    query_best_substitute = Produit.select().where(
        Produit.unique_id == query_best_id)
    query_store = (
        Magasin.select()
        .join(Produit_magasin)
        .where(Produit_magasin.produit_unique_id == query_best_id)
    )
    list_store = []
    for store in query_store:
        list_store.append(store.nom_magasin)

    for product in query_best_substitute:
        if query_best_nutriscore:
            print(
                "votre substitut ",
                product.nutriscore,
                product.nom_produit,
                product.url,
                list_store,
                product.description,
            )
        else:
            print(
                """il n'y a pas de produit plus sain mais voici un 
                équivalent: """,
                product.nutriscore,
                product.nom_produit,
                product.url,
                list_store,
                product.description,
            )
    return query_best_id


def my_db_substitute_setter(id_choice):
    new_favorite, created = Favoris.get_or_create(
        fk_unique_id_produit=id_choice)
