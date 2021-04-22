# Projet5
projet openclassrooms P5, Open food facts
The goal of the program is to interact with Open Food Facts database to recover the foods,
compare them and offer the user a healthier substitute for the food they want


## START
This project uses Python and Requests library. It is advisable to use
a virtual environment to avoid conflicts with other version of libraries.


## pre requirement
to start the game, you need:
* Python
* Git
* Requests library (auto install later with requirements)


## INSTALLATION

1. Download sources from github repository:
[link to github repo](https://github.com/Jinr0h404/Projet5.git)

You can dowload zip file or dowload with the url and Git:
- create new folder for Project, with Git in root of the folder
- Make git clone https://github.com/Jinr0h404/Projet5.git

1. If you don't have it: Install Python 3.9 and requirements file.
You will find the sources for Python here:
[link to sources](https://www.python.org/downloads/)

1. **Strongly advised:**
Install a virtual environment like Pipenv:
install with command: `pip install pipenv`
to use pipenv: 
in project folder, init virtual env with command: `pipenv shell`
when you are in your virtual environment you can install libraries from requirements
file with command: `pip install -r requirements.txt`


## Application

To start the application
* In the virtual env
* start the main file with command: `python main.py`

## Result

During the first use the open food fact database is downloaded and a database with the
recovered products is created.
Then during new launches of the application, we have the choice between recreating the 
database or using the previous one.


## PROJECT

made with:
* Python 3.9.0
* Sublime Text
* requests==2.25.1
* mysql-connector==2.2.9
* peewee==3.14.4
* PyMySQL==1.0.2
* tqdm==4.59.0
* API Open Food Facts

## Contributor & Author

Ewen Jeannenot