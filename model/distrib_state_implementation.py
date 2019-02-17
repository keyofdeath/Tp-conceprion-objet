#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

from .distrib_state import DistrbState

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/distrib_state_implementation.log",
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


class InsererCarte(DistrbState):

    def __init__(self, distrib):
        """
        :param distrib: (Distrib) distributeur
        """
        super().__init__(distrib)

    def inserer_carte(self, card_number):
        """
        Méthode pour inserer une carte dans la machine. Puis met dans l'attribut carte_inseree la carte inserée.
        :param card_number: (string) Numéro de ma carte inserée
        :return: (bool) True la carte est trouvée. False la carte n'a pas été trouvée
        """
        self.distrib.carte_inseree = self.distrib.banque.rechercher_carte(card_number)
        PYTHON_LOGGER.info("Carte inserée: {}".format(self.distrib.carte_inseree))
        if self.distrib.carte_inseree is not None:
            self.distrib.distrib_state = SaisireCode(self.distrib)
            return True
        return False


class SaisireCode(DistrbState):

    def __init__(self, distrib):
        """
        :param distrib: (Distrib) distributeur
        """
        super().__init__(distrib)

    def saisire_code(self, code):
        """
        Regarde si le code saisi est correct
        :param code: (string) code entré
        :return: (bool) True code correct sinon False
        """
        res = self.distrib.carte_inseree.code_ok(code) and self.distrib.banque.client_de_banque_numero_carte(
            self.distrib.carte_inseree.obtenir_numero_carte())
        if res:
            self.distrib.distrib_state = Menu(self.distrib)
        else:
            self.distrib.distrib_state = InsererCarte(self.distrib)
        return res


class Menu(DistrbState):

    def __init__(self, distrib):
        """
        :param distrib: (Distrib) distributeur
        """
        super().__init__(distrib)

    def menu(self, action):
        """
        Menu ou l'utilisateur choisie se qu'il veut faire
        :param action: (int) Utiliser les constantes dans la classe Distrib
        :return: (object) Retourn les infos en fonction de l'action choisie
        """
        if action == self.distrib.CONSULTATION:
            self.distrib.distrib_state = AttentComptChoisit(self.distrib)
            return self.distrib.banque.consultation(self.distrib.carte_inseree.obtenir_numero_carte())
        else:
            self.distrib.distrib_state = AttenteInformationTransfer(self.distrib)


class AttentComptChoisit(DistrbState):

    def __init__(self, distrib):
        """
        :param distrib: (Distrib) distributeur
        """
        super().__init__(distrib)

    def attente_compt_choisit(self, acount_number):
        """
        Fonction pour obtenir les données d'un compte.
        :param acount_number: (string) numero du compte
        :return: (Dictionnaire) info sur le compte en dictionnaire [numéro, solde, operations]
        """
        compte = self.distrib.banque.consulter_compte(acount_number)
        if compte is None:
            return None
        historique_str = [str(operation) for operation in compte.historique_operation]
        compt = {"numero": compte.obtenir_rib(), "solde": compte.solde, "operations": historique_str}
        self.distrib.distrib_state = ComptAfficher(self.distrib)
        return compt


class ComptAfficher(DistrbState):

    def __init__(self, distrib):
        """
        :param distrib: (Distrib) distributeur
        """
        super().__init__(distrib)

    def compt_afficher(self):
        """
        Pour retourner aux menu une fois la consultation des compts fini
        """
        self.distrib.distrib_state = Menu(self.distrib)


class AttenteInformationTransfer(DistrbState):

    def __init__(self, distrib):
        """
        :param distrib: (Distrib) distributeur
        """
        super().__init__(distrib)

    def attente_information_transfer(self, acount_number, credit_to_transfer):
        """
        Recupaire les informations entrée pas l'utilisateur est attend qu'il valide
        :param acount_number: (int) Numeros de compt a créditer
        :param credit_to_transfer: (float) Montant a transferer
        """
        self.distrib.distrib_state = ConfirmerVirement(self.distrib, acount_number, credit_to_transfer)


class ConfirmerVirement(DistrbState):

    def __init__(self, distrib, acount_number, credit_to_transfer):
        """
        :param distrib: (Distrib) distributeur
        :param acount_number: (int) Numeros de compt a créditer
        :param credit_to_transfer: (float) Montant a transferer
        """
        super().__init__(distrib)
        self.acount_number = acount_number
        self.credit_to_transfer = credit_to_transfer

    def confimer_le_virement(self, confirm_transfer):
        """
        L'utilisateur valide les information entrée on effectue le transfer
        :param confirm_transfer: (bool) True confirm le transfer
        :return: (bool) True transfer effectuer
        """
        res = False
        if confirm_transfer:
            res = self.distrib.banque.virement(self.acount_number, self.credit_to_transfer,
                                               self.distrib.carte_inseree.obtenir_numero_carte())

        self.distrib.distrib_state = Menu(self.distrib)
        return res
