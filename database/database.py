#! /usr/bin/env python3
# coding: utf-8

""" the database module contains the different classes for update database
and functions to manage the database"""

import peewee
import mysql.connector
import database.model
from tqdm import tqdm


mysql_db = peewee.MySQLDatabase(
    "api_open_test", user="food", password="1234", host="localhost"
)

def my_db_connect():
    mysql_db.connect()


def my_db_category_getter():
    #mysql_db.connect()
    query = database.model.Categorie.select().order_by(peewee.fn.Rand()).limit(15)
    list_id_cat = []
    for cat in query:
        number_product = (
            database.model.Produit.select()
            .join(database.model.Produit_categorie)
            .where(database.model.Produit_categorie.categorie_unique_id == cat.unique_id)
        )
        print(
            "l'id de catégorie n°:",
            cat.unique_id,
            "représente la categorie : ",
            cat.nom_categorie,
            "et contient",
            len(number_product),
            "produit",
        )
        list_id_cat.append(cat.unique_id)
    return list_id_cat


def my_db_product_getter(id_choice):
    #mysql_db.connect()
    # query = Produit.select().where(Produit.nutriscore == 'A')
    query = (
        database.model.Produit.select()
        .join(database.model.Produit_categorie)
        .where(database.model.Produit_categorie.categorie_unique_id == id_choice)
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
    #mysql_db.connect()
    query = database.model.Produit.select().where(database.model.Produit.unique_id == id_prod)
    product_name = []
    for product in query:
        product_name.append(product.nom_produit)
    return product_name[0]


def my_db_substitute_getter(id_choice):
    #mysql_db.connect()
    list_substitute = {}
    query_cat = (
        database.model.Categorie.select()
        .join(database.model.Produit_categorie)
        .where(database.model.Produit_categorie.produit_unique_id == id_choice)
    )
    for category in query_cat:
        query_substitute = (
            database.model.Produit.select()
            .join(database.model.Produit_categorie)
            .where(
                database.model.Produit_categorie.categorie_unique_id == category.unique_id)
        )
        for product in query_substitute:
            if product.unique_id in list_substitute.keys():
                list_substitute[product.unique_id] += 1
            else:
                list_substitute[product.unique_id] = 1
    sorted_dict = sorted(list_substitute.items(
        ), key=lambda t: t[1], reverse=True)
    i = 1
    query = database.model.Produit.select().where(database.model.Produit.unique_id == id_choice)
    query_nutriscore = ""
    query_best_id = 0
    query_same_id = 0
    query_best_nutriscore = ""
    query_same_nutriscore = ""
    for product in query:
        query_nutriscore = product.nutriscore

    while not query_best_nutriscore and not query_same_nutriscore:
        while i < len(sorted_dict) and not query_best_nutriscore:
            query_best = database.model.Produit.select().where(
                database.model.Produit.unique_id == sorted_dict[i][0])
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
                query_best = database.model.Produit.select().where(
                    database.model.Produit.unique_id == sorted_dict[i][0]
                )
                for product in query_best:
                    query_same_nutr_temp = product.nutriscore
                    query_same_id_temp = product.unique_id
                if query_same_nutr_temp == query_nutriscore:
                    query_same_nutriscore = query_same_nutr_temp
                    query_best_id = query_same_id_temp
                else:
                    i += 1

    query_best_substitute = database.model.Produit.select().where(
        database.model.Produit.unique_id == query_best_id)
    query_store = (
        database.model.Magasin.select()
        .join(database.model.Produit_magasin)
        .where(database.model.Produit_magasin.produit_unique_id == query_best_id)
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
    #mysql_db.connect()
    new_favorite, created = database.model.Favoris.get_or_create(
        fk_unique_id_produit=id_choice)
