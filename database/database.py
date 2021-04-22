#! /usr/bin/env python3
# coding: utf-8

""" the database module contains the different class and methods for update
and manage the database"""

import peewee
import mysql.connector
import database.model
from tqdm import tqdm


""" use peewee, define which database and user is used"""
mysql_db = peewee.MySQLDatabase(
    "api_open_test", user="food", password="1234", host="localhost"
)

class Data_manager:
    """this class allows you to make queries on the database"""
    def __init__(self):
        self.list_id_cat = []
        self.list_id_prod = []
        self.prod_name = ''
        self.best_id = 0



    def my_db_connect():
        """ method to initiate the connection to the database"""
        mysql_db.connect()
    
    
    def my_db_category_getter(self):
        """method which executes a query returning a random list of 15
        categories (the list contains the id of the categories) taken from
        the database"""
        query = database.model.Category.select().order_by(
            peewee.fn.Rand()).limit(15)
        list_id_cat = []
        for cat in query:
            number_product = (
                database.model.Product.select()
                .join(database.model.Product_category)
                .where(database.model.Product_category.category_unique_id ==
                    cat.unique_id)
            )
            print(
                "l'id de catégorie n°:",
                cat.unique_id,
                "représente la categorie : ",
                cat.category_name,
                "et contient",
                len(number_product),
                "produit",
            )
            list_id_cat.append(cat.unique_id)
        return list_id_cat


    def my_db_product_getter(self, id_choice):
        """method which executes a query returning the list of products
        contained in the category whose id is given as a parameter."""
        query = (
            database.model.Product.select()
            .join(database.model.Product_category)
            .where(database.model.Product_category.category_unique_id ==
                id_choice)
        )
        list_id_prod = []
        for product in query:
            print(
                "l'id de produit n°:",
                product.unique_id,
                "représente : ",
                product.product_name,
                "dont le nutriscore est: ",
                product.nutriscore,
                )
            list_id_prod.append(product.unique_id)
        return list_id_prod


    def my_db_product_name_getter(self, id_prod):
        """method which executes a query returning the name of products
        whose id is given as a parameter."""
        query = database.model.Product.select().where(
            database.model.Product.unique_id == id_prod)
        product_name = []
        for product in query:
            product_name.append(product.product_name)
        self.prod_name = product_name[0]


    def my_db_substitute_getter(self, id_choice):
        """method which executes a query returning a possible substitute for
        the product whose id is given as a parameter. If there is no product
        with a better nutriscore then the first product in the list of
        products belonging to a maximum of common categories is selected."""
        list_substitute = {}
        query_cat = (
            database.model.Category.select()
            .join(database.model.Product_category)
            .where(database.model.Product_category.product_unique_id ==
                id_choice)
        )
        for category in query_cat:
            query_substitute = (
                database.model.Product.select()
                .join(database.model.Product_category)
                .where(
                    database.model.Product_category.category_unique_id ==
                    category.unique_id)
            )
            """loop to give +1 each time a product has a same category of
            the choose product"""
            for product in query_substitute:
                if product.unique_id in list_substitute.keys():
                    list_substitute[product.unique_id] += 1
                else:
                    list_substitute[product.unique_id] = 1
        """function for sorted list by value (unique id of item)"""
        sorted_dict = sorted(list_substitute.items(
            ), key=lambda t: t[1], reverse=True)
        i = 1
        query = database.model.Product.select().where(
            database.model.Product.unique_id == id_choice)
        query_nutriscore = ""
        query_best_id = 0
        query_same_id = 0
        query_best_nutriscore = ""
        query_same_nutriscore = ""
        for product in query:
            query_nutriscore = product.nutriscore

        while not query_best_nutriscore and not query_same_nutriscore:
            while i < len(sorted_dict) and not query_best_nutriscore:
                query_best = database.model.Product.select().where(
                    database.model.Product.unique_id == sorted_dict[i][0])
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
                    query_best = database.model.Product.select().where(
                        database.model.Product.unique_id == sorted_dict[i][0]
                    )
                    for product in query_best:
                        query_same_nutr_temp = product.nutriscore
                        query_same_id_temp = product.unique_id
                    if query_same_nutr_temp == query_nutriscore:
                        query_same_nutriscore = query_same_nutr_temp
                        query_best_id = query_same_id_temp
                    else:
                        i += 1

        query_best_substitute = database.model.Product.select().where(
            database.model.Product.unique_id == query_best_id)
        query_store = (
            database.model.Store.select()
            .join(database.model.Product_store)
            .where(database.model.Product_store.product_unique_id ==
                query_best_id)
        )
        list_store = []
        for store in query_store:
            list_store.append(store.store_name)

        for product in query_best_substitute:
            if query_best_nutriscore:
                print(
                    "votre substitut pourrait être: ",
                    product.product_name ,'\n',
                    "son nutriscore est : ",
                    product.nutriscore, '\n',
                    "petite description: ",
                    product.description, '\n',
                    "vous pouvez le trouver dans les magasins: ",
                    ", ".join(list_store), '\n',
                    "lien vers le site open food fact: ",
                    product.url
                )
            else:
                print(
                    """il n'y a pas de produit plus sain mais voici un 
équivalent: """,
                    product.product_name ,'\n',
                    "son nutriscore est : ",
                    product.nutriscore, '\n',
                    "petite description: ",
                    product.description, '\n',
                    "vous pouvez le trouver dans les magasins: ",
                    ", ".join(list_store), '\n',
                    "lien vers le site open food fact: ",
                    product.url
                )
        self.best_id = query_best_id

    def my_db_substitute_setter(self, id_choice):
        """method which executes a query to add the id of the chosen product
        in the favorites table if it is not already there"""
        new_favorite, created = database.model.Favorites.get_or_create(
            fk_unique_id_product=id_choice)

    def my_db_favorites(self):
        """method that executes a query to display the list of products in
        the favorites table."""
        query_favorite = database.model.Favorites.select().join(
            database.model.Product)
        print("voici vos favoris: ")

        for id_prod in query_favorite:
            query_product = database.model.Product.select().join(
                database.model.Favorites).where(
            database.model.Product.unique_id == id_prod.fk_unique_id_product)
            for product in query_product:
                print(
                    "\nnom du produit: ",
                    product.product_name,
                    "petite description: ",
                    product.description,
                    "lien vers le site open food fact: ",
                    product.url
                )
