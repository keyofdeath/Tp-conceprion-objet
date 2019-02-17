#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/Carte.log",
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


class Carte:

    def __init__(self, numero_carte, code):
        """
        Creation d'une carte
        :param numero_carte: (string) Numéro de la carte
        :param code: (string) Code de la carte
        """
        self.numero_carte = numero_carte
        self.code = code

    def obtenir_numero_carte(self):
        """
        Retourne le numero de la carte
        :return: (string) le numero de la carte
        """
        return self.numero_carte

    def code_ok(self, code):
        """
        Controle si le code est valide
        :param code: (string) code entré par l'utilisateur
        :return: (bool) True si le code est valide sinon False
        """
        return code == self.code

    def __str__(self):
        """
        ToString
        :return:(string) Retourne le ToString de la carte
        """
        return "Numero carte: {}, Code {}".format(self.numero_carte, self.code)
