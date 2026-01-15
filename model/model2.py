import networkx as nx
from database.dao2 import DAO

# Mappatura difficoltà --> fattore
FATTORE_DIFFICOLTA = {
    "facile" : 1.0,
    "media" : 1.5,
    "difficile" : 2.0
}

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.rifugi = None # Dizionario con tutti i nodi che rispettano "anno" <= year
        self.connessioni = None # Dizionario con tutte le connessioni
        self.G = nx.Graph()


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # Prendo i rifugi
        rifugi = DAO.get_all_rifugi(year)

        # Prendo le connessioni
        connessioni = DAO.get_connessioni(rifugi, year)

        # Pulisco il grafo e lo ricreo
        self.G.clear()

        # Aggiungo i nodi(oggetti rifugio)
        self.G.add_nodes_from(self.rifugi.values())

        # Aggiungo gli archi pesati
        for c in self.connessioni.values():
            r1,r2 = c.r1, c.r2
            peso = self._calcola_peso(c)
            if peso is not None:
                self.G.add_edge(r1, r2, weight=peso)

    def _calcola_peso(self, c):
        """
        Calcola il peso di un arco: distanza * fattore difficoltà.
        Se i dati non sono validi, ritorna None.
        :param c: connessioni dei rifugi
        :return: peso dell'arco
        """
        try:
            distanza = float(getattr(c, "distanza"))
        except Exception:
            return None # Segnala che l'arco non deve essere inserito

        difficolta = getattr(c, "difficolta")
        if difficolta not in FATTORE_DIFFICOLTA:
            return None # difficoltà non valida

        fattore = FATTORE_DIFFICOLTA[difficolta]
        return distanza * fattore


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        pesi = [d["weight"] for _, _, d in self.G.edges(data=True)]
        if not pesi:
            return None, None
        return min(pesi), max(pesi)

        # altro modo mio
        pesi = []
        for r1, r2, attr in self.G.edges(data=True):
            peso = attr["weight"]
            if peso is not None:
                pesi.append(peso)
        return min(pesi), max(pesi)

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori = 0
        maggiori = 0
        for r1, r2, attr in self.G.edges(data=True):
            if attr["weight"] < soglia:
                minori += 1
            else:
                maggiori += 1
        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def shortes_path_dijkistra(self, soglia):
        """
        Restituisce la lista di nodi del cammino minimo (somma dei pesi minima) il cui percorso è fatto
        solo da archi con peso > soglia. Se non esiste alcun percorso valido restituisce [].
        :param soglia: il cammino minimo individuato deve essere fatto da archi il cui peso deve essere > soglia
        :return: il cammino minimo come lista di archi [(u,v,attr), ...] oppure []
        """

        # Crea un sottografo con soli archi validi
        edges_ok = []

        for u, v, attr in self.G.edges(data=True):
            peso = attr.get("weight")
            if peso is not None and peso > soglia:
                edges_ok.append((u, v))

        # controllo DOPO il ciclo
        if not edges_ok:
            return []

        H = self.G.edge_subgraph(edges_ok).copy()
        nodes = list(H.nodes())
        if len(nodes) < 2:
            return []

        best_cost = float("inf")
        best_edges = []

        for nodo in nodes:
            lenght, path = nx.single_source_dijkstra(H, nodo, weight="weight")
            # Restituisce 2 dizionari
            # lenght = {nodo_arrivo : peso_minimo}
            # path = {nodo_arrivo : lista_nodi}
            for n_arrivo, costo in lenght.items():
                if nodo.id >= n_arrivo.id or costo >= best_cost:
                    continue
                path_nodes = path.get(n_arrivo)
                if not path_nodes or len(path_nodes) < 3:
                    continue
                # converti i nodi in archi con attributi
                edges_list = []
                for u, v in zip(path_nodes, path_nodes[1:]):
                    attr = H.get_edge_data(u, v) # or self.G.get_edge_data(u, v)
                    edges_list.append((u, v, attr))
                best_cost = costo
                best_edges = edges_list
            return best_edges

    def shortest_path_recursive(self, soglia):
        """
        Restituisce la lista di nodi del cammino minimo (somma dei pesi minima) il cui percorso è fatto
        solo da archi con peso > soglia. Se non esiste alcun percorso valido restituisce [].
        :param soglia: il cammino minimo individuato deve essere fatto da archi il cui peso deve essere > soglia
        :return: il cammino minimo come lista di archi [(u,v,attr), ...] oppure []
        """
        # Stato per la ricerca
        self.best_edges = [] # Lista di archi (u, v, attr) della migliore soluzione trovata
        self.best_cost = float("inf") # Costo minimo trovato

        # Avvia la ricerca da ogni nodo
        for n in self.G.nodes():
            parziale = [n]
            parziale_edges = []
            self._ricorsione(parziale, parziale_edges, soglia)

        return self.best_edges

    def _ricorsione(self, parziale, parziale_edges, soglia):
        """
        Ricorsione che esplora i percorsi semplici composti da archi con peso > soglia
        :param parziale: lista di nodi già considerati nel cammino
        :param parziale_edges: lista di archi già considerati nel cammmino
        :param soglia: il cammino minimo individuato deve essere fatto da archi il cui peso deve essere > soglia
        """
        # Valuta SEMPRE il cammino corrente
        if parziale_edges:
            cost = self.compute_weight_path(parziale_edges)

            # Pruning
            if cost >= self.best_cost:
                return
                # con il return evito di continuare a calcolare questi cammini inutilmente

            # Cammino valido come Dijkstra
            if len(parziale_edges) >=2:
                self.best_cost = cost
                self.best_edges = parziale_edges

        n_last = parziale[-1]
        neighs = self._get_admissible_neighbors(n_last, parziale, soglia)

        for n in neighs:
            edge_attr = self.G.get_edge_data(n_last, n)
            parziale.append(n)
            parziale_edges.append((n,n_last,edge_attr))
            self._ricorsione(parziale, parziale_edges, soglia)
            parziale.pop()
            parziale_edges.pop()

    def _get_admissible_neighbors(self, ultimo_nodo, parziale_nodes, soglia):
        """
        Restituisce i vicini ammissibili:
        - non ancora visitati (evita cicli)
        - l'arco (ultimo_nodo, v) esiste e ha 'weight' > soglia
        :param ultimo_nodo: il nodo da considerare
        :param parziale_nodes: lista di nodi già considerati nel cammino
        :param soglia: il cammino minimo individuato deve essere fatto da archi il cui peso deve essere > soglia
        :return: lista di vicini ammissibili
        """
        neighs = []
        for v in self.G.neighbors(ultimo_nodo):
            # controllo che il vicino non sia già in parziale
            if v in parziale_nodes:
                continue
            attr = self.G.get_edge_data(ultimo_nodo, v)
            # controllo che l'arco abbia il dizionario attr
            if not attr:
                continue
            w = attr.get("weight",None) # se weight non esiste restituisce none
            # controllo che esista weight e non sia quindi None
            if w is None:
                continue
            # ora considero solo archi con peso maggiore della soglia
            if w > soglia:
                neighs.append(v)
        return neighs



    def compute_weight_path(self, parziale_edges):
        """
        Somma i pesi della lista "edges"
        :param: parziale_edges: lista di archi
        :return: la somma dei pesi di ogni arco
        """
        total = 0.0
        for u, v, attr in parziale_edges:
            if attr:
                total += float(attr.get("weight", 0.0))
        return total