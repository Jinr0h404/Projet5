#! /usr/bin/env python3
# coding: utf-8

""" the main is used to execute the script, it creates the database
and gives elements for the ui display"""

import api.downloader
import database.model
import database.database
import ui.ui


def main():
    # generate an instance of Database object contain a list of product from the api open food fact
    data = api.downloader.Database()
    data.list_database()
    get_list = data.product_list
    data.cleaner_list(get_list)
    # create database in mysql
    db = database.model.Database_creation()
    db.my_db_create()
    db.my_db_setter(data.clean_list)
    #generate instance of Data_manager
    data_manage = database.database.Data_manager()
    # generate an instance of Menu object from the UI
    menu = ui.ui.Menu()
    menu.run(menu, data_manage)



if __name__ == "__main__":
    """execute main function of thie file if he is run like main program"""
    main()
