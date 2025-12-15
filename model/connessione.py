from dataclasses import dataclass

# classi create per rappresentare dei dati
@dataclass
class Connessione:
    _id : int
    _id_rifugio1 : int
    _id_rifugio2 : int
    _distanza : float
    _difficolta : str
    _durata : str
    _anno : int

    # metodo per leggere la fermata (getter)
    @property
    def id(self): # -> int (lo scrive pycharm ma superfluo)
        return self._id

    @property
    def id_rifugio1(self):
        return self._id_rifugio1

    @property
    def id_rifugio2(self):
        return self._id_rifugio2

    @property
    def distanza(self):
        return self._distanza

    @property
    def difficolta(self):
        return self._difficolta

    @property
    def durata(self):
        return self._durata

    @property
    def anno(self):
        return self._anno

   # funzione per stampare

    def __str__(self):
        return f'Connessione({self._id}, {self._id_rifugio1}, {self._id_rifugio2}, {self._distanza}, {self._difficolta}, {self._durata}, {self._anno})'

    def __hash__(self):
        return hash(self._id)