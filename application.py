#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import abc
import json
import logging.handlers
import os

from flask import Flask, render_template, redirect, request, url_for, session
from flask_assets import Bundle, Environment

from model import Compte, Client, Carte, Distrib, Banque

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/application.log",
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

app = Flask(__name__)

app.secret_key = "zefzarega5zerg+6e5rzeafz"

env = Environment(app)
js = Bundle('js/clarity-icons.min.js', 'js/clarity-icons-api.js',
            'js/clarity-icons-element.js', 'js/custom-elements.min.js')
env.register('js_all', js)
css = Bundle('css/clarity-ui.min.css', 'css/clarity-icons.min.css', 'css/overwrite.css')
env.register('css_all', css)

CLIENT_DATA_BASE = os.path.join('.', 'bank_data_base.json')


class State(metaclass=abc.ABCMeta):
    """
    Interface pour définir les différent état de l'interface
    """

    @abc.abstractmethod
    def handle(self):
        pass


class InsererCarte(State):
    """
    L'utilisateur a entrer le numeros de carte
    Next state: SaisirCode
    """

    def handle(self):
        if request.method == "POST":
            attempted_card_number = request.form['card_number']
            if dab_model.distrib.inserer_carte(attempted_card_number):
                session['card_number'] = request.form['card_number']
                return SaisirCode(), render_template("saisir_code.html")
        return self, render_template('index.html')


class SaisirCode(State):
    """
    L'utilisateur a entrer le code de la carte
    Next state: Menu
    """

    def handle(self):
        if request.method == "POST":
            attempted_password = request.form['password']
            if dab_model.distrib.saisire_code(attempted_password):
                session['logged_in'] = True
                session['wrong_pass'] = False
                return Menu(), render_template('menu.html')
            else:
                session['logged_in'] = False
                session['wrong_pass'] = True
        return InsererCarte(), render_template('index.html')


class Menu(State):
    """
    L'utilisateur a choisie sont operation
    Next state: TransferInformationWait ou AttenteCompteChoisit
    """

    def handle(self):

        if request.method == "POST":
            if "money_transfer" in request.form:
                dab_model.distrib.menu(dab_model.distrib.TRANSFER)
                return TransferInformationWait(), render_template('transfer_form.html')
            else:
                acount_names = dab_model.distrib.menu(dab_model.distrib.CONSULTATION)
                if acount_names is None:
                    return Menu(), render_template('menu.html', message="Error !")
                return AttenteCompteChoisit(acount_names), render_template('attente_choix_compt.html',
                                                                           acount_names=acount_names)
        return self, render_template('menu.html')


class AttenteCompteChoisit(State):
    """
    L'utilisateur a choisie le compt a consulter
    Next state: CompteAffiches
    """

    def __init__(self, acount_names):
        self.acount_names = acount_names

    def handle(self):

        if request.method == "POST":
            compt_information = dab_model.distrib.attente_compt_choisit(request.form["acount_number"])
            if compt_information is None:
                return Menu(), render_template('menu.html', message="Error compt nom trouver !")
            return CompteAffiches(compt_information), render_template('compte_afficher.html',
                                                                      acount_info=compt_information)

        return self, render_template('attente_choix_compt.html', acount_names=self.acount_names)


class CompteAffiches(State):
    """
    L'utilisateur a fini de visualiser le compt
    Next state: Menu
    """

    def __init__(self, compt_information):
        self.compt_information = compt_information

    def handle(self):
        if request.method == "POST":
            dab_model.distrib.distrib_state.compt_afficher()
            return Menu(), render_template('menu.html')

        return CompteAffiches(self.compt_information), render_template('compte_afficher.html',
                                                                       acount_info=self.compt_information)


class TransferInformationWait(State):
    """
    L'utilisateur a entrer les informations pour le transfer
    Next state: ConfirmTransfer
    """

    def handle(self):
        if request.method == "POST":
            dab_model.distrib.attente_information_transfer(request.form["account_number"],
                                                           int(request.form["amount"]))
            return ConfirmTransfer(request.form), render_template('confirm_transfer.html', result=request.form)
        return self, render_template('transfer_form.html')


class ConfirmTransfer(State):
    """
    L'utilisateur a valider le transfer
    Next state: Menu
    """

    def __init__(self, transfer_information):
        self.transfer_information = transfer_information

    def handle(self):
        if request.method == "POST":
            if "validation" in request.form:
                if dab_model.distrib.confimer_le_virement(True):
                    return Menu(), render_template('menu.html', message="Virement ok")
                else:
                    return Menu(), render_template('menu.html', message="Error !")
            else:
                dab_model.distrib.confimer_le_virement(False)
                return Menu(), render_template('menu.html', message="Virement annuler")
        redirect(url_for("homepage"))


class DabModel:
    """
    Model pour contenir l'instence du distributeur
    """

    def __init__(self, first_state):
        """
        :param first_state: (State) State de depart
        """
        self._state = first_state
        self._first_state = self._state

        with open(CLIENT_DATA_BASE) as f:
            data_base = json.load(f)

        list_client = []

        # on charge les clients de la base de donnée
        for client in data_base:
            list_client.append(Client(Carte(client["card-number"], client["card-password"]),
                                      *[Compte(compt["name"], compt["sold"]) for compt in client["bank-accounts"]]))

        self.banque = Banque(*list_client)
        self.distrib = Distrib(self.banque)

    def request(self):
        """
        Request fait par l'utilisateur
        :return: reponce HTML
        """
        next_state, state_result = self._state.handle()
        self._state = next_state
        return state_result

    def reset(self):
        """
        Reset l'etat du distributeur
        :return: reponce HTML
        """
        self._state = self._first_state
        session.clear()
        session['logged_in'] = False
        self.distrib.cancel()
        return redirect(url_for("homepage"))


dab_model = DabModel(SaisirCode())


@app.route('/', methods=["GET", "POST"])
def homepage():
    return dab_model.request()


@app.route('/cancel')
def cancel():
    return dab_model.reset()
