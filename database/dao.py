from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connessione


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO

    def __init__(self):
        pass

    # funzione che legge tutti i dati della tabella rifugi
    @staticmethod
    def read_all_rifugi():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary = True)
        query = "SELECT * FROM rifugio "
        cursor.execute(query)
        for row in cursor: # row è un dizionario
            rifugio = Rifugio(row["id"], row["nome"], row["localita"], row["altitudine"], row["capienza"])
            results.append(rifugio)
        cursor.close()
        conn.close()
        return results
        #lista di oggetti di tipo fermata

    @staticmethod
    def read_all_connessioni(anno):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary = True)
        query = "SELECT * FROM connessione WHERE anno <= %s "
        cursor.execute(query,(anno,))
        for row in cursor:
            connessione = Connessione(row["id"], row["id_rifugio1"], row["id_rifugio2"],
                           row["distanza"], row["difficolta"],
                            row["durata"], row["anno"])
            results.append(connessione)
        cursor.close()
        conn.close()
        return results
