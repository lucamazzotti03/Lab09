from copy import deepcopy

import model
from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO
import copy

class Model:
    def __init__(self):
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        # TODO: Aggiungere eventuali altri attributi
        self._tour_attrazioni = {}


        # Caricamento
        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni():
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()

    def load_tour(self):
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()

    def load_attrazioni(self):
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()

    def load_relazioni(self):
        """
            Interroga il database per ottenere tutte le relazioni fra tour e attrazioni e salvarle nelle strutture dati
            Collega tour <-> attrazioni.
            --> Ogni Tour ha un set di Attrazione.
            --> Ogni Attrazione ha un set di Tour.
        """

        # TODO
        self._tour_attrazioni = TourDAO.get_tour_attrazioni()

        for tr in self.tour_map:
            for tourattr in self._tour_attrazioni:
                if tourattr["id_tour"] == tr:
                    for attrazione in self.attrazioni_map:
                        if tourattr["id_attrazione"] == attrazione:
                            self.tour_map[tr].attrazioni.add(self.attrazioni_map[attrazione])


            print(tr, self.tour_map[tr].attrazioni)
        for attrazione in self.attrazioni_map:
            for tourattr in self._tour_attrazioni:
                if tourattr["id_attrazione"] == attrazione:
                    for tr in self.tour_map:
                        if tourattr["id_tour"] == tr:
                            self.attrazioni_map[attrazione].tour.add(self.tour_map[tr])
            print(attrazione, self.attrazioni_map[attrazione].tour)






    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """
        Calcola il pacchetto turistico ottimale per una regione rispettando i vincoli di durata, budget e attrazioni uniche.
        :param id_regione: id della regione
        :param max_giorni: numero massimo di giorni (può essere None --> nessun limite)
        :param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)

        :return: self._pacchetto_ottimo (una lista di oggetti Tour)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il valore culturale del pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1

        # TODO

        if max_giorni is None:
            max_giorni = float("inf")
        if max_budget is None:
            max_budget = float("inf")

        self._max_giorni = max_giorni
        self._max_budget = max_budget
        self._tour_regione = []

        for tour in self.tour_map:
            if self.tour_map[tour].id_regione == id_regione:
                self._tour_regione.append(tour)

        self._ricorsione(0, [], 0, 0, 0, set())

        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list, durata_corrente: int, costo_corrente: float, valore_corrente: int, attrazioni_usate: set):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""

        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno

        if start_index == len(self._tour_regione):
            if valore_corrente > self._valore_ottimo:
                self._valore_ottimo = valore_corrente
                self._costo = costo_corrente
                self._pacchetto_ottimo = pacchetto_parziale.copy()
            return

        id_tour = self._tour_regione[start_index]
        tour = self.tour_map[id_tour]
        if costo_corrente + tour.costo <= self._max_budget and durata_corrente + tour.durata_giorni <= self._max_giorni:
            attrazioni_ok = True
            for attrazione in tour.attrazioni:
                if attrazione.id in attrazioni_usate:
                    attrazioni_ok = False
                    break
            if attrazioni_ok:
                valore_nuovo = valore_corrente
                nuove_attrazioni = attrazioni_usate.copy()
                for attrazione in tour.attrazioni:
                    valore_nuovo += attrazione.valore_culturale
                    nuove_attrazioni.add(attrazione.id)
                pacchetto_parziale.append(tour)

                self._ricorsione(start_index + 1, pacchetto_parziale, durata_corrente + tour.durata_giorni, costo_corrente + tour.costo, valore_nuovo, nuove_attrazioni)

                pacchetto_parziale.pop()

        self._ricorsione(start_index + 1, pacchetto_parziale, durata_corrente, costo_corrente, valore_corrente, attrazioni_usate)















