import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def handle_cammino_minimo(self, e):

        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return


        self._view.lista_visualizzazione_3.controls.clear()
        (lista_cammini) =  self._model.search_cammino_minimo(soglia)
        print("Cammini trovati: ", len(lista_cammini))

        for cammino in lista_cammini:
            testo = ""  # riga per il cammino corrente
            for i in range(0, len(cammino)-1):
                rifugio_1 = self._model._dizionario_rifugi[cammino[i]]
                rifugio_2 = self._model._dizionario_rifugi[cammino[i+1]]
                testo += (f"[{rifugio_1.id}] {rifugio_1.nome} ({rifugio_1.localita}) "
                          f"--> [{rifugio_2.id}] {rifugio_2.nome} ({rifugio_2.localita})"
                          f"[Peso {self._model.G[rifugio_1.id][rifugio_2.id]['weight']}]")

                self._view.lista_visualizzazione_3.controls.append(ft.Text(testo))

        self._view.page.update()




