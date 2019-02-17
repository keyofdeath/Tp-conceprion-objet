#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/DistribState.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class DistrbState:

    def __init__(self, distrib):
        """
        :param distrib: (Distrib) distributeur
        """
        self.distrib = distrib

    def inserer_carte(self, card_number):
        """
        Méthode pour inserer une carte dans la machine. Puis met dans l'attribut carte_inseree la carte inserée.
        :param card_number: (string) Numéro de ma carte inserée
        :return: (bool) True la carte est trouvée. False la carte n'a pas été trouvée
        """
        raise Exception("Inserer carte: Can call this function in this state")

    def saisire_code(self, code):
        """
        Regarde si le code saisi est correct
        :param code: (string) code entré
        :return: (bool) True code correct sinon False
        """
        raise Exception("Saisire Code: Can call this function in this state")

    def menu(self, action):
        """
        Menu ou l'utilisateur choisie se qu'il veut faire
        :param action: (int) Utiliser les constantes dans la classe Distrib
        :return: (object) Retourn les infos en fonction de l'action choisie
        """
        raise Exception("Menu: Can call this function in this state")

    def attente_compt_choisit(self, acount_number):
        """
        Fonction pour obtenir les données d'un compte.
        :param acount_number: (string) numero du compte
        :return: (Dictionnaire) info sur le compte en dictionnaire [numéro, solde, operations]
        """
        raise Exception("Attente compt Choisit: Can call this function in this state")

    def compt_afficher(self):
        """
        Pour retourner aux menu une fois la consultation des compts fini
        """
        raise Exception("Compt afficher: Can call this function in this state")

    def attente_information_transfer(self, acount_number, credit_to_transfer):
        """
        Recupaire les informations entrée pas l'utilisateur est attend qu'il valide
        :param acount_number: (int) Numeros de compt a créditer
        :param credit_to_transfer: (float) Montant a transferer
        """
        raise Exception("Attente information virement: Can call this function in this state")

    def confimer_le_virement(self, confirm_transfer):
        """
        L'utilisateur valide les information entrée on effectue le transfer
        :param confirm_transfer: (bool) True confirm le transfer
        :return: (bool) True transfer effectuer
        """
        raise Exception("Confirmer le virement: Can call this function in this state")
