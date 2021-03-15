#! /usr/bin/env python3
# coding: utf-8


import api.getData, database.dataScript

def main():
    data = api.getData.Database()
    #print(data.product_list)
    #print(len(data.product_list))
    data.list_database()
    #print(data.product_list)
    #print(len(data.product_list))
    test = data.product_list
    data.cleaner_list(test)
    print(data.clean_list)
    print(len(data.clean_list))
    database.dataScript.my_db_create()
    database.dataScript.my_db_getter(data.clean_list)

if __name__ == "__main__":
    """execute main function of thie file if he is run like main program"""
    main()
