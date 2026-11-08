from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""
#viene effettuato l'accesso al database e viene costruito il primo menù a tendina

class BibliotecaDAO:
    def __init__(self):
        pass

    def get_all_biblioteche(self) -> list[Biblioteca]:
        #chiedo la connessione dalla pool
        cnx=DBConnect.get_connection()
        if cnx is None:
            return []   #restituisce una lista vuota = nessun risultato

        #creo il cursore a dizionario:
        cursor = cnx.cursor(dictionary=True)
        #scrivo una query per le biblioteche in ordine alfabetico:
        query= "SELECT * FROM biblioteca ORDER BY nome"
        cursor.execute(query)

        #lista di DTO:
        result = []
        for row in cursor:
            #creo l'oggetto biblioteca a partire dal file in sql:
            b=Biblioteca(id=row["id"], nome=row["nome"], indirizzo=row["indirizzo"])
            result.append(b)

        cursor.close()
        cnx.close()
        return result