import copy

import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._lista_rifugi = []
        self._dizionario_rifugi = {}
        self._rifugi_visitati = set()
        self._rifugi_vicini = []

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO

        self.G.clear()
        self._dizionario_rifugi.clear()

        # carico i rifugi e costruisco il dizionario
        rifugi = DAO.read_all_rifugi()
        self._lista_rifugi = rifugi
        for rifugio in self._lista_rifugi:
            self._dizionario_rifugi[rifugio.id] = rifugio
            self.G.add_node(rifugio.id)

        # leggo le connessioni
        lista_connessioni = DAO.read_all_connessioni(year)

        for c in lista_connessioni:
            u_nodo = self._dizionario_rifugi[c.id_rifugio1]
            v_nodo = self._dizionario_rifugi[c.id_rifugio2]

            if c.difficolta == "facile":
                fattore_difficolta = 1.0
            elif c.difficolta == "media":
                fattore_difficolta = 1.5
            else:
                fattore_difficolta = 2.0
            peso = float(c.distanza) * float(fattore_difficolta)

            self.G.add_edge(u_nodo.id, v_nodo.id, weight=peso)


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """

        max_peso = 0
        min_peso = 2930

        for u, v, data in self.G.edges (data = True):
            if data["weight"] > max_peso:
                max_peso = data["weight"]
            elif data["weight"] < min_peso:
                min_peso = data["weight"]
        return min_peso, max_peso

        # TODO

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO

        n_minori = 0
        n_maggiori = 0
        for u, v, data in self.G.edges (data = True):
            if data["weight"] < soglia:
                n_minori += 1
            elif data["weight"] > soglia:
                n_maggiori += 1
        return n_minori, n_maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    # secondo metodo

    def search_cammino_minimo(self, soglia):
        self._rifugi_visitati = set()
        self._cammino_minimo = [] # qui salvo tutti i cammini con peso minimo
        self._peso_minimo = float("inf")

        for nodo in self.G.nodes:
            # nodo = id del rifugio
            somma = 0
            self.ricorsione([], nodo, somma, soglia)

        return self._cammino_minimo

    def ricorsione(self, lista_parziale, nodo_corrente, somma, soglia):

        # aggiungo il nodo corrente alla soluzione parziale e alla lista
        # dei nodi visitati
        lista_parziale.append(nodo_corrente)
        self._rifugi_visitati.add(nodo_corrente)

        # prima condizione terminale:
        # se questa combinazione è già maggiore del self._peso_minimo non serve
        # andare avanti con il cammino, senza soffermasi su questi rami,
        # ma conviene rimuovere l'ultimo rifugio e provarne un altro
        if somma > self._peso_minimo:
            lista_parziale.pop()
            self._rifugi_visitati.remove(nodo_corrente)
            return

        # verifico vincoli
        if len(lista_parziale) >= 3: # almeno tre nodi
            if somma < self._peso_minimo:
                self._peso_minimo = somma
                self._cammino_minimo = [copy.deepcopy(lista_parziale)]
            elif somma == self._peso_minimo:
                self._cammino_minimo.append(copy.deepcopy(lista_parziale))
                # devo usare copy se no i cammini cambiano da soli ogni volta che faccio
                # il backtracking

        # continuo a esplorare
        # passo ricorsivo
        for vicino in self.G.neighbors(nodo_corrente):
            if vicino not in self._rifugi_visitati:
                peso = self.G[nodo_corrente][vicino]["weight"]
                if peso > soglia:
                    self.ricorsione(lista_parziale, vicino, somma + peso, soglia)

        #backstracking generale
        self._rifugi_visitati.remove(nodo_corrente)
        lista_parziale.pop()
        # va fuori il ciclo dei vicini perchè quando finisco tutte
        # le sue ramificazioni posso togliere il nodo corrente

        # primo metodo
        # floyd-warshall

    def cammino_minimo_nx(self, soglia):
        """
        Calcola tutti i cammini minimi tra coppie di nodi, restituisce
        una lista di cammini minimi (lista di liste)
        """
        # inizializzo
        self._cammino_minimo = []
        self._peso_minimo = float("inf")

        # creo un sotto_grafo contenente solo gli archi che hanno un peso che supera la soglia
        G_filtrato = nx.Graph()
        for u, v, attr in list(self.G.edges(data = True)):
            peso = attr["peso"]
            if peso > soglia:
                G_filtrato.add_edge(u, v, weight = peso)

        # calcolo cammino minimo
        for sorgente, cammino_minimo in nx.all_pairs_dijkstra(G_filtrato, weight = "peso"):
            # si ottiene una tupla (sorgente, dizionario)
            # sorgente: nodo di partenza, cammino_minimo = dizionario che lega ogni
            # nodo raggiungibile al percorso più breve
            for target, percorso in cammino_minimo.items():
                if len(percorso) >= 3:
                    # per calcolare il peso totale del percorso
                    costo = nx.path_weight(G_filtrato, percorso, weight = "peso")
                    if costo < self._peso_minimo:
                        self._peso_minimo = costo
                        self._cammino_minimo = percorso
