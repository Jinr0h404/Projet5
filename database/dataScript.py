#! /usr/bin/env python3
# coding: utf-8

import requests, json


"""retrieve a list of products in JSON format through Open Food Fact API"""
class Database:
	def __init__(self):
		self.product_list = []
		self.pages = 10
		self.json = 1
		self.page_size = 5
		self.request_url = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=yahourt"

	def list_database(self):
		i = 1
		for i in range(1, self.pages):
			r = requests.get(self.request_url + '&page_size='+str(self.page_size)+'&page='+str(i)+'&json='+str(self.json))
			data_json = r.json()
			for product in data_json['products']:
				"""generate a list of dict where each dict = a product"""
				self.product_list.append(
					{
					'name': product.get('product_name_fr'),
					'brand': product.get('brands'),
					'store': product.get('stores').split(','),
					'category': product.get('categories').split(','),
					'nutriscore' : product.get('nutrition_grade_fr'),
					'description' : product.get('generic_name_fr')
					}
					)
			i+=1



# a tester
#print(r.status_code)
#if r.status_code == 200:
#    print('You got the success!')
#elif r.status_code == 404:
#    print('Page not Found.')