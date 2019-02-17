# Dab TP Conception objet
BLANC Swan & LE BRAS Clément

## Installation

Installation de python 3

    sudo apt install virtualenv
    sudo apt install python3-pip
   
Creation d'un environement virtuiel python3 & installation des requirements

    virtualenv -p python3 venv
    . venv/bin/activate
    pip install -r requirements.txt

## Start

Pour Linux

    export FLASK_APP=application.py
    flask run

Pour Windows

    set FLASK_APP=application.py
    flask run
    

## Base de donnée de la banque

Voici a quoi resemble un cient dans notre base de donnée json


    {
        "card-number": (string) numeros de la carte,
        "card-password": (string) mots de passe de la carte,
        "bank-accounts": [ list de tout les comptes poséder par le client
          {
            "name": (string) nom du compt,
            "sold": (float) sold du compt
          },
          ...
        ]
    }

Vous pouvez rajouter, modifier suprimer des client en modifiant le fichier `bank_data_base.json`
