#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .distrib_state_implementation import *

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/Distrib.log",
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


class Distrib:
    TRANSFER = 0
    CONSULTATION = 1

    def __init__(self, banque):
        """
        :param banque: (Banque) Banque ratachée au distributeur
        """
        self.banque = banque
        self.carte_inseree = None
        self.distrib_state = InsererCarte(self)

    def inserer_carte(self, card_number):
        """
        Méthode pour inserer une carte dans la machine. Puis met dans l'attribut carte_inseree la carte inserée.
        :param card_number: (string) Numéro de ma carte inserée
        :return: (bool) True la carte est trouvée. False la carte n'a pas été trouvée
        """
        return self.distrib_state.inserer_carte(card_number)

    def saisire_code(self, code):
        """
        Regarde si le code saisi est correct
        :param code: (string) code entré
        :return: (bool) True code correct sinon False
        """
        return self.distrib_state.saisire_code(code)

    def menu(self, action):
        """
        Menu ou l'utilisateur choisie se qu'il veut faire
        :param action: (int) Utiliser les constantes dans la classe Distrib
        :return: (object) Retourn les infos en fonction de l'action choisie
        """
        return self.distrib_state.menu(action)

    def attente_compt_choisit(self, acount_number):
        """
        Fonction pour obtenir les données d'un compte.
        :param acount_number: (string) numero du compte
        :return: (Dictionnaire) info sur le compte en dictionnaire [numéro, solde, operations]
        """
        return self.distrib_state.attente_compt_choisit(acount_number)

    def compt_afficher(self):
        """
        Pour retourner aux menu une fois la consultation des compts fini
        """
        return self.distrib_state.compt_afficher()

    def attente_information_transfer(self, acount_number, credit_to_transfer):
        """
        Recupaire les informations entrée pas l'utilisateur est attend qu'il valide
        :param acount_number: (int) Numeros de compt a créditer
        :param credit_to_transfer: (float) Montant a transferer
        """
        return self.distrib_state.attente_information_transfer(acount_number, credit_to_transfer)

    def confimer_le_virement(self, confirm_transfer):
        """
        L'utilisateur valide les information entrée on effectue le transfer
        :param confirm_transfer: (bool) True confirm le transfer
        :return: (bool) True transfer effectuer
        """
        return self.distrib_state.confimer_le_virement(confirm_transfer)

    def cancel(self):
        """
        Si on veut annuler l'operation on revien aux debut
        """
        self.distrib_state = InsererCarte(self)
