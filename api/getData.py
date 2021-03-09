#! /usr/bin/env python3
# coding: utf-8

import requests, json


"""retrieve a list of products in JSON format through Open Food Fact API"""
class Database:
    def __init__(self):
        self.product_list = []
        self.pages = 10
        self.json = 1
        self.page_size = 100
        self.request_url = "https://fr.openfoodfacts.org/cgi/search.pl"
        self.clean_list = []

    def list_database(self):
        for i in range(1, self.pages):
            params = {
            "action":"process",
            "page_size":self.page_size,
            "page":i,
            "json":self.json
            }
            r = requests.get(self.request_url, params)
            data_json = r.json()
            for product in data_json['products']:
                if product.get('product_name_fr') and product.get('categories') and product.get('nutrition_grade_fr') and product.get('stores'):
                    """generate a list of dict where each dict = a product"""
                    self.product_list.append(
                        {
                        'name': product.get('product_name_fr').lower(),
                        'brand': product.get('brands').lower(),
                        'store': product.get('stores').lower().split(','),
                        'category': product.get('categories').lower().split(','),
                        'nutriscore' : product.get('nutrition_grade_fr').upper(),
                        'description' : product.get('generic_name_fr')
                        }
                        )

    def cleaner_list(self, test):
        temp_list = []
        for i in test:
            if i['name'] not in temp_list:
                self.clean_list.append(i)
                temp_list.append(i['name'])




# a tester
#print(r.status_code)
#if r.status_code == 200:
#    print('You got the success!')
#elif r.status_code == 404:
#    print('Page not Found.')