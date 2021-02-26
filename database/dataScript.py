#! /usr/bin/env python3
# coding: utf-8

import requests, json


"""retrieve a list of products in JSON format through Open Food Fact API"""
r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=yahourt&page_size=2&page=1&json=true")
#print(r.json())
test = r.json()
#print(test['products'])
product_list = []
for product in test['products']:
	"""generate a list of dict where each dict = a product"""
	product_list.append(
		{
		'name': product.get('product_name_fr').lower(),
		'brand': product.get('brands').lower(),
		'store': product.get('stores').lower().split(','),
		'category': product.get('categories').lower().split(','),
		'nutriscore' : product.get('nutrition_grade_fr').upper(),
		'description' : product.get('generic_name_fr').lower()
		}
		)


print(product_list)


# a tester
#print(r.status_code)
#if r.status_code == 200:
#    print('You got the success!')
#elif r.status_code == 404:
#    print('Page not Found.')