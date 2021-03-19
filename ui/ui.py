#! /usr/bin/env python3
# coding: utf-8

from peewee import *
import mysql.connector, database.dataScript

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
            choice= input("1 - Quel aliment souhaitez-vous remplacer ? \n2 - Retrouver mes aliments substitués.\n")
        self.home = int(choice)
        return(self.home)

    def choice_display(self, list_cat_id):
        print('les produits de quelle catégorie souhaitez-vous afficher ?')
        choice = "0"
        choice_input = 0
        while not(choice_input in list_cat_id):
            choice = input("entrez le numéro de la catégorie qui vous intéresse\n")
            if choice.isdigit() == True:
                choice_input = int(choice)
            else:
                print("il faut entrer un nombre")
                    #choice = input("entrez le numéro de la catégorie qui vous intéresse\n")
        self.category = choice_input
        return(self.category)


    def product_display(self, list_prod_id):
        print("Pour quel produit souhaitez vous un substitut?")
        choice = "0"
        choice_input = 0
        while not(choice_input in list_prod_id):
            choice = input("entrez le numéro du produit qui vous intéresse\n")
            if choice.isdigit() == True:
                choice_input = int(choice)
            else:
                print("il faut entrer un nombre")
                    #choice = input("entrez le numéro de la catégorie qui vous intéresse\n")
        self.product = choice_input
        return(self.product)

    def substitute_display(self, product_name, new_product):
        print("En remplacement de ", product_name, "vous pouvez utiliser: ")
        print(new_product)
        choice = input("souhaitez-vous enregistrer ce produit comme substitut dans vos favoris? \n1 - OUI\n2 - NON\n")
        if choice == "1":
            print("vous pouvez maintenant retrouver ce produit dans votre liste de favoris")
        else:
            print("la prochaine fois")
        self.favorites = int(choice)



def main():
    menu = Menu()
    choice_result = menu.home_display()
    if choice_result == 1:
        print("tu vas voir toutes mes catégories")
    else:
        print("voici tes aliments favoris")
    database.dataScript.my_db_connect()
    query = produit.select().where(produit.nutriscore == 'A')




if __name__ == "__main__":
    """execute main function of thie file if he is run like main program"""
    main()