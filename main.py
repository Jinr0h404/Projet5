#! /usr/bin/env python3
# coding: utf-8

""" the main is used to execute the script, it creates the database
and gives elements for the ui display"""

import api.downloader
import database.model
import ui.ui


def main():
    data = api.downloader.Database()
    data.list_database()
    test = data.product_list
    data.cleaner_list(test)
    database.model.my_db_create()
    database.model.my_db_setter(data.clean_list)
    menu = ui.ui.Menu()
    choice_result = menu.home_display()
    if choice_result == 1:
        display_cat_choice = database.model.my_db_category_getter()
        display_prod_choice = database.model.my_db_product_getter(
            menu.choice_display(display_cat_choice)
        )
        prod_to_substitute = menu.product_display(display_prod_choice)
        substitute = database.model.my_db_substitute_getter(
            prod_to_substitute)
        substitute_choice = menu.substitute_record(
            database.model.my_db_product_name_getter(prod_to_substitute),
            substitute,
        )
        if menu.favorites:
            database.model.my_db_substitute_setter(substitute)
    else:
        database.model.substitute_display()
        database.model.my_db_product_getter(1)


if __name__ == "__main__":
    """execute main function of thie file if he is run like main program"""
    main()
