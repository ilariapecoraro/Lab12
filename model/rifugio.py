from dataclasses import dataclass

# classi create per rappresentare dei dati
@dataclass
class Rifugio:
    _id : int
    _nome : str
    _localita : str
    _altitudine : int
    _capienza : int

    # metodo per leggere la fermata (getter)
    @property
    def id(self): # -> int (lo scrive pycharm ma superfluo)
        return self._id

    @property
    def nome(self): # -> str:
        return self._nome

    @property
    def localita(self):
        return self._localita

    @property
    def altitudine(self):
        return self._altitudine

    @property
    def capienza(self):
        return self._capienza

   # funzione per stampare

    def __str__(self):
        return f'Rifugio({self._id}, {self._nome}, {self._localita}, {self._altitudine}, {self._capienza})'

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return self.id == other.id