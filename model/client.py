#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/ClientDeBanque.log",
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


class Client:

    def __init__(self, carte, *liste_compte):
        """
        Consructeur
        :param carte: (Carte) Carte du client
        :param liste_compte: (List of Compte) Liste des comptes
        """
        self.carte = carte
        self.liste_compte = liste_compte

    def proprietaire_de_carte(self, numero_carte):
        """
        Fonction indiquant si une carte appartient à ce client en fonction de son numéro
        :param numero_carte: (String) Numero de la carte
        :return: (boolean) True si le numero correspond sinon False
        """
        return numero_carte == self.carte.obtenir_numero_carte()

    def obtenir_liste_compte(self):
        """
        Renvoie la liste des comptes de ce client
        :return: (list of Compte) Tous les comptes de ce client
        """
        return self.liste_compte

    def obtenir_compte_rib(self, rib):
        """
        Obtient le compte associé au RIB donné
        :param rib: (string) RIB / numero de compte à chercher
        :return: (Compte) Le compte associé au rib, None si aucun compte n'est trouvé
        """
        for compte in self.liste_compte:
            if compte.obtenir_rib() == rib:
                return compte
        return None

    def obtenir_carte(self):
        """
        Renvoie la carte de ce client
        :return: (carte) La carte de ce client
        """
        return self.carte
