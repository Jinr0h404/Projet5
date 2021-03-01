#! /usr/bin/env python3
# coding: utf-8


import database.dataScript

def main():
	data = database.dataScript.Database()
	print(data.product_list)
	print(len(data.product_list))
	data.list_database()
	print(data.product_list)
	print(len(data.product_list))

if __name__ == "__main__":
	"""execute main function of thie file if he is run like main program"""
	main()