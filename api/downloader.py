#! /usr/bin/env python3
# coding: utf-8

""" the getData module contains a classe and methods to get all elements
information from the api openfoodfact"""

import requests
import json
from tqdm import tqdm



class Database:
    """the database class takes as attribute the request elements on the
    openfoodfact API"""
    def __init__(self):
        self.product_list = []
        self.pages = 5
        self.json = 1
        self.page_size = 50
        self.request_url = "https://fr.openfoodfacts.org/cgi/search.pl"
        self.clean_list = []

    def list_database(self):
        """retrieve a list of products in JSON format through Open Food Fact
        API. The loop goes through each element of the number of pages given,
        checks if the main categories are correctly entered for the product
        and creates a dictionary list."""
        for i in tqdm(range(1, self.pages)):# tqdm add progress bar
            params = {
                "action": "process",
                "page_size": self.page_size,
                "page": i,
                "json": self.json,
            }
            r = requests.get(self.request_url, params)
            data_json = r.json()
            for product in data_json["products"]:
                if (
                    product.get("product_name_fr")
                    and product.get("categories")
                    and product.get("nutrition_grade_fr")
                    and product.get("stores")
                ):
                    """generate a list of dict where each dict = a product"""
                    self.product_list.append(
                        {
                            "name": product.get("product_name_fr").lower(),
                            "brand": product.get("brands").lower(),
                            "store": product.get("stores").lower().split(","),
                            "category": product.get(
                                "categories").lower().split(","),
                            "nutriscore": product.get(
                                "nutrition_grade_fr").upper(),
                            "description": product.get("generic_name_fr"),
                            "url": product.get("url"),
                        }
                    )

    def cleaner_list(self, list_to_clean):
        """this method loops over the first dictionary list to remove
        duplicates"""
        temp_list = []
        for i in list_to_clean:
            if i["name"] not in temp_list:
                self.clean_list.append(i)
                temp_list.append(i["name"])
