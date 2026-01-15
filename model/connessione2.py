from dataclasses import dataclass
import datetime
from model.rifugio import Rifugio

@dataclass
class Connessione:
    r1 : Rifugio
    r2 : Rifugio
    distanza : float
    difficolta : int
    durata : datetime.time = datetime.time(0, 0, 0)


    def __str__(self):
        return (f"Connessione: {self.r1.nome} - {self.r2.nome},"
                f"distanza: {self.distanza} km, difficolta: {self.difficolta},"
                f"tempo: {self.durata}")

    def __repr__(self):
        return (f"Connessione: {self.r1.nome} - {self.r2.nome},"
                f"distanza: {self.distanza} km, difficolta: {self.difficolta},"
                f"tempo: {self.durata}")