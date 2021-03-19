#! /usr/bin/env python3
# coding: utf-8


import api.getData, database.dataScript, ui.ui

def main():
    data = api.getData.Database()
    #print(data.product_list)
    #print(len(data.product_list))
    data.list_database()
    #print(data.product_list)
    #print(len(data.product_list))
    test = data.product_list
    data.cleaner_list(test)
    #print(data.clean_list)
    print(len(data.clean_list))
    database.dataScript.my_db_create()
    database.dataScript.my_db_setter(data.clean_list)
    menu = ui.ui.Menu()
    choice_result = menu.home_display()
    if choice_result == 1:
        display_cat_choice = database.dataScript.my_db_category_getter()
        display_prod_choice = database.dataScript.my_db_product_getter(menu.choice_display(display_cat_choice))
        prod_to_substitute = menu.product_display(display_prod_choice)
        menu.substitute_display(database.dataScript.my_db_product_name_getter(prod_to_substitute), 'test')
    else:
        database.dataScript.my_db_product_getter(1)




if __name__ == "__main__":
    """execute main function of thie file if he is run like main program"""
    main()
