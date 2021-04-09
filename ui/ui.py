#! /usr/bin/env python3
# coding: utf-8


""" the ui module contains a classe and methods for manage the display of the
user interface"""


from database import database

class Menu:
    def __init__(self):
        self.home = 0
        self.category = 0
        self.product = 0
        self.favorites = 0

    def home_display(self):
        print('Hey on cherche un produit sain')
        choice = ""
        while not(choice == "1" or choice == "2"):
            choice = input("1 - Quel aliment souhaitez-vous remplacer ?\n"
                "2 - Retrouver mes aliments substitués.\n")
            if not choice.isdigit():
                print("il faut entrer un chiffre de la liste")
        self.home = int(choice)
#        return(self.home)

    def choice_display(self, list_cat_id):
        choice = "0"
        choice_input = 0
        while not(choice_input in list_cat_id):
            choice = input(
                "Choisissez la catégorie dont vous vouler afficher les produits\n")
            if choice.isdigit() is True:
                choice_input = int(choice)
            else:
                print("il faut entrer un nombre")
        self.category = choice_input
        return(self.category)

    def product_display(self, list_prod_id):
        print("Pour quel produit souhaitez vous un substitut?")
        choice = "0"
        choice_input = 0
        while not(choice_input in list_prod_id):
            choice = input("entrez le numéro du produit qui vous intéresse\n")
            if choice.isdigit() is True:
                choice_input = int(choice)
            else:
                print("il faut entrer un nombre")
        self.product = choice_input
#        return(self.product)

    def substitute_record(self):
        choice = "0"
        choice_input = 0
        while not(choice_input == 1 or choice_input == 2):
            choice = input(
                "souhaitez-vous enregistrer ce substitut dans vos favoris?\n"
                "1 - OUI\n"
                "2 - NON\n")
            if choice.isdigit() is True:
                choice_input = int(choice)
            else:
                print("il faut entrer un nombre")
        if choice_input == 1:
            print(
                "vous pouvez maintenant retrouver ce produit dans vos favoris"
                )
        else:
            print("la prochaine fois")
        self.favorites = choice_input

    def substitute_display(self):
        print("voici la liste de vos favoris")

    def run(self, menu, data_manage):
        quit = 0
        while not quit:
            choice_result = menu.home_display()
            if self.home == 1:
                display_cat_choice = data_manage.my_db_category_getter()
                display_prod_choice = data_manage.my_db_product_getter(
                    menu.choice_display(display_cat_choice)
                )
                menu.product_display(display_prod_choice)
                data_manage.my_db_substitute_getter(self.product)
                substitute = data_manage.best_id
                data_manage.my_db_product_name_getter(self.product)
                menu.substitute_record()
                if menu.favorites:
                    data_manage.my_db_substitute_setter(substitute)
            else:
                menu.substitute_display
                data_manage.my_db_favorites()
            quit_choice = ""
            while not(quit_choice == "0" or quit_choice == "1"):
                quit_choice = input(
                    "souhaitez-vous continuer?\n"
                    "0 - OUI\n"
                    "1 - NON\n")
                if quit_choice.isdigit() is True:
                    quit = int(quit_choice)
                else:
                    print("il faut entrer un chiffre")






def main():
    pass


if __name__ == "__main__":
    """execute main function of thie file if he is run like main program"""
    main()
