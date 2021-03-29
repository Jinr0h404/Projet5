#! /usr/bin/env python3
# coding: utf-8


""" the ui module contains a classe and methods for manage the display of the
user interface"""


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
        self.home = int(choice)
        return(self.home)

    def choice_display(self, list_cat_id):
        print('les produits de quelle catégorie souhaitez-vous afficher ?')
        choice = "0"
        choice_input = 0
        while not(choice_input in list_cat_id):
            choice = input(
                "entrez le numéro de la catégorie qui vous intéresse\n")
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
        return(self.product)

    def substitute_record(self, product_name, new_product):
        print("En remplacement de ", product_name, "vous pouvez utiliser: ")
        print(new_product)
        choice = input(
            "souhaitez-vous enregistrer ce substitut dans vos favoris?"
            "1 - OUI\n"
            "2 - NON\n")
        if choice == "1":
            print(
                "vous pouvez maintenant retrouver ce produit dans vos favoris"
                )
        else:
            print("la prochaine fois")
        self.favorites = int(choice)

    def substitute_display(self):
        print("voici la liste de vos favoris")


def main():
    pass


if __name__ == "__main__":
    """execute main function of thie file if he is run like main program"""
    main()
