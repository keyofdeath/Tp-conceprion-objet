#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import logging.handlers
import os

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/Operation.log",
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


class Operation:
    RETRAIT = "retrait"
    CREDIT = "credit"

    def __init__(self, operation, value):
        """
        Constructeur
        :param operation: (string) identifiant de l'operation (voir constantes)
        :param value: (int) montant de l'operation
        """
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.operation = operation
        self.value = value

    def __str__(self):
        """
        ToString
        :return:(string) Retourne le ToString de l'operation
        """
        return "[{}] {}: {}$".format(self.operation, self.date, self.value)
