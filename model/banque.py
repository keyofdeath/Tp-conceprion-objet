#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/Banque.log",
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


class Banque:

    def __init__(self, *client):
        """
        Contructeur
        :param client: (List of Client) Liste de client
        """
        self.list_client = client

    def virement(self, rib, montant, numero_carte):
        """
        Effectue un virement pour des clients de la même banque
        :param rib: (string) numero de compte à créditer
        :param montant: (int) montant à créditer
        :param numero_carte: (string) numéro de carte à débiter
        :return: (bool) True si le virement est fait sinon False
        """
        if self.client_de_banque_rib(rib):
            compte_destination = self.rechercher_compte_rib(rib)
            compte_expeditaire = self.rechercher_compte_carte(numero_carte)[0]
            if compte_expeditaire.solde_suffisant(montant):
                compte_expeditaire.retrait(montant)
                compte_destination.crediter(montant)
                return True
        return False

    def consultation(self, numero_carte):
        """
        Renvoie les numéros de compte de la carte associée
        :param numero_carte:(string) numéro de la carte
        :return: (list de string) Liste des numéros de compte. Renvoie None si il n'y a aucun numéro
        """
        compte_list = self.rechercher_compte_carte(numero_carte)
        return [compte.obtenir_rib() for compte in compte_list] if compte_list is not None else None

    def consulter_compte(self, numero_compte):
        """
        Fonction pour obtenir un compte en fonction de son numéro
        :param numero_compte: (string) numéro de compte
        :return: (compte) Compte associé au numéro de carte
        """
        for client in self.list_client:
            compte = client.obtenir_compte_rib(numero_compte)
            if compte is not None:
                return compte
        return None

    def rechercher_compte_carte(self, numero_carte):
        """
        Renvoie les comptes de la carte
        :param numero_carte: (string) numéro de la carte
        :return: (list de compte) List des comptes. Renvoie None si aucun compte n'est trouvé
        """
        for client in self.list_client:
            if client.proprietaire_de_carte(numero_carte):
                return client.obtenir_liste_compte()
        return None

    def rechercher_carte(self, numero_carte):
        """
        Fonction pour obtenir une carte en fonction de son numéro
        :param numero_carte: (string) numéro de la carte
        :return: (Carte) carte associé au numéro de carte
        """
        for client in self.list_client:
            if client.proprietaire_de_carte(numero_carte):
                return client.obtenir_carte()
        return None

    def client_de_banque_numero_carte(self, numero_carte):
        """
        Regarde en fonction du numéro de carte du client s'il est un client de cette banque
        :param numero_carte: (string) numéro de la carte
        :return: (boolean) True si le client est dans cette banque, False sinon
        """
        for client in self.list_client:
            if client.proprietaire_de_carte(numero_carte):
                return True
        return False

    def client_de_banque_rib(self, rib):
        """
        Regarde en fonction du RIB du client s'il est un client de cette banque
        :param rib: (string) le RIB / numéro de compte du client
        :return: (boolean) True si le client est dans cette banque, False sinon
        """

        for client in self.list_client:
            if client.obtenir_compte_rib(rib) is not None:
                return True
        return False

    def rechercher_compte_rib(self, rib):
        """
        Renvoie les comptes du RIB
        :param rib: (string) RIB / numéro de compte du client
        :return: (compte) compte associé à ce RIB
        """
        for client in self.list_client:
            compte = client.obtenir_compte_rib(rib)
            if compte is not None:
                return compte
        return None
