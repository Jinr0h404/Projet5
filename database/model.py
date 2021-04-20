#! /usr/bin/env python3
# coding: utf-8

""" the model module contains the different classes for create database
with ORM peewee"""

import peewee
import mysql.connector
from tqdm import tqdm


""" use peewee, define which database and user is used"""
mysql_db = peewee.MySQLDatabase(
    "api_open_food", user="food", password="1234", host="localhost"
)


class BaseModel(peewee.Model):
    """the parent BaseModel class is used to give the default Meta attributes
    (the engine of the table and the encoding) to the other classes"""
    class Meta:
        database = mysql_db
        table_settings = ["ENGINE=InnoDB", "DEFAULT CHARSET=utf8"]


class Product(BaseModel):
    """this class is for the peewee orm, it gives the parameters for the
    creation of the table of the same name in the database."""
    unique_id = peewee.AutoField()
    product_name = peewee.CharField(200)
    brand = peewee.TextField(null=True)
    description = peewee.TextField(null=True)
    nutriscore = peewee.CharField(1)
    url = peewee.TextField(null=True)


class Category(BaseModel):
    """this class is for the peewee orm, it gives the parameters for the
    creation of the table of the same name in the database."""
    unique_id = peewee.AutoField()
    category_name = peewee.CharField(200)


class Product_category(BaseModel):
    """this class is for the peewee orm, it gives the parameters for the
    creation of the table of the same name in the database."""
    product_unique_id = peewee.ForeignKeyField(Product)
    category_unique_id = peewee.ForeignKeyField(Category)

    class Meta:
        primary_key = peewee.CompositeKey("product_unique_id",
            "category_unique_id")


class Store(BaseModel):
    """this class is for the peewee orm, it gives the parameters for the
    creation of the table of the same name in the database."""
    unique_id = peewee.AutoField()
    store_name = peewee.CharField(100)


class Product_store(BaseModel):
    """this class is for the peewee orm, it gives the parameters for the
    creation of the table of the same name in the database."""
    product_unique_id = peewee.ForeignKeyField(Product)
    store_unique_id = peewee.ForeignKeyField(Store)

    class Meta:
        primary_key = peewee.CompositeKey("product_unique_id",
            "store_unique_id")


class Favorites(BaseModel):
    """this class is for the peewee orm, it gives the parameters for the
    creation of the table of the same name in the database."""
    fk_unique_id_product = peewee.ForeignKeyField(Product)


class Database_creation:
    """this class contains the methods to create the database using the
    mysql.connector library and the tables with peewee orm."""
    def __init__(self):
        self.db_connexion = mysql.connector.connect(
            user="root", password="12345678", host="localhost",
            buffered=True
            )
        self.exist_bdd = 0

    def my_db_check(self):
        """ this method check if there is already tables in bdd and return an
        empty row if not."""
        cursor = self.db_connexion.cursor()
        cursor.execute("""SELECT TABLE_NAME FROM
            information_schema.tables WHERE
            table_schema = 'api_open_food';""")
        bdd_check = cursor.fetchone()
        if bdd_check:
            self.exist_bdd = 1

    def my_db_create(self):
        """ this method uses mysql.connector to create the database and a
        non-root user to manage this database.""" 
        """ creating database_cursor to perform SQL operation """
        cursor = self.db_connexion.cursor()
        """executing cursor with execute method and pass SQL query"""
        cursor.execute("DROP DATABASE IF EXISTS api_open_food;")
        cursor.execute("CREATE DATABASE IF NOT EXISTS api_open_food")
        cursor.execute("""CREATE USER IF NOT EXISTS 'food'@'localhost'
            IDENTIFIED BY '1234'""")
        cursor.execute("""GRANT ALL PRIVILEGES ON api_open_food.* TO 
            'food'@'localhost'""")

    def my_db_setter(self, list_dict):
        """ this method uses peewee to create the database tables and their
        columns""" 
        mysql_db.create_tables(
            [Product, Category, Product_category, Store, Product_store,
                Favorites]
        )

        for i in tqdm(list_dict):
            """tqdm add loading tool progression"""
            new_product = Product.create(
                product_name=i["name"],
                brand=i["brand"],
                description=i["description"],
                nutriscore=i["nutriscore"],
                url=i["url"],
            )
            for category in i["category"]:
                """the value of the category key in the dictionary can contain
                several elements. I therefore loop on the category to fill my
                table with get_or_create function of peewee to haven't a
                duplicate"""
                category = category.strip()
                """ strip() remove spaces before and after item"""
                new_category, created = Category.get_or_create(
                    category_name=category)
                id_product = Product.select(Product.unique_id).where(
                    Product.product_name == i["name"]
                )
                id_category = Category.select(Category.unique_id).where(
                    Category.category_name == category
                )
                res = Product_category.insert(
                    product_unique_id=id_product,
                    category_unique_id=id_category).execute()
            """ make a loop for each store"""
            for store in i["store"]:
                """like category, the value of the store key in the dictionary
                can contain several elements. loop to fill my table with the
                get_or_create function"""
                store = store.strip()
                new_store, created = Store.get_or_create(store_name=store)
                id_product = Product.select(Product.unique_id).where(
                    Product.product_name == i["name"]
                )
                id_magasin = Store.select(Store.unique_id).where(
                    Store.store_name == store
                )
                res = Product_store.insert(
                    product_unique_id=id_product, store_unique_id=id_magasin
                ).execute()


