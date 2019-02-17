#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

from .operation import Operation

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/Compt.log",
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


class Compte:

    def __init__(self, rib, solde):
        """
        Constructeur
        :param rib: (String) Rib du compte
        :param solde: (int) Quantité d'argent du le compte en $
        """
        self.rib = rib
        self.solde = solde
        self.historique_operation = []

    def solde_suffisant(self, montant):
        """
        Regarde si le solde est suffisant pour realiser un debit
        :param montant: (int) montant a débiter
        :return: (bool) True le solde est sufisant sinon False
        """
        return self.solde - montant >= 0

    def retrait(self, montant):
        """
        Fonction qui effectue un retrait sur ce compte
        :param montant: (int) quantite d'argent à retirer en $
        :return: Rien
        """
        self.solde -= montant
        self.historique_operation.append(Operation(Operation.RETRAIT, montant))
        PYTHON_LOGGER.info("Retrait de {} nouveux solde {}".format(montant, self.solde))

    def crediter(self, montant):
        """
        Fonction qui effectue un credit sur ce compte
        :param montant: (int) quantite d'argent à crediter
        :return: Rien
        """
        self.solde += montant
        self.historique_operation.append(Operation(Operation.CREDIT, montant))
        PYTHON_LOGGER.info("Credit de {} nouveaux solde {}".format(montant, self.solde))

    def obtenir_rib(self):
        """
        Renvoie le numero de ce compte: son RIB
        :return: (string) Le numero / RIB de ce compte
        """
        return self.rib

    def __str__(self):
        """
        ToString
        :return:(string) Retourne le ToString du compte
        """
        historique_str = [str(operation) for operation in self.historique_operation]
        historique_str = "\n\t\t".join(historique_str)
        return "***Compt {}***\n\tSolde {}\n\tHistorique opération\n\t\t{}".format(self.rib, self.solde, historique_str)
