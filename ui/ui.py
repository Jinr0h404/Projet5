#! /usr/bin/env python3
# coding: utf-8

class Menu:
	def __init__(self):
		self.home = 0
		self.category = []
		self.product = []
		self.favorites = []

	def home_display(self):
		print('Hey on cherche un produit sain')
		choice = ""
		while not(choice == "1" or choice == "2"):
			choice= input("1 - Quel aliment souhaitez-vous remplacer ? \n2 - Retrouver mes aliments substitués.\n")
		self.home = int(choice)
		return(self.home)



def main():
	menu = Menu()
	menu.home_display()
	print(menu.home)
	if menu.home == 1:
		print("tu vas voir toutes mes catégories")
	else:
		print("voici tes aliments favoris")



if __name__ == "__main__":
    """execute main function of thie file if he is run like main program"""
    main()