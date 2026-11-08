from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    def get_all_generi(self) -> list[str]:
        cnx=DBConnect.get_connection()
        if cnx is None:
            return []

        cursor=cnx.cursor(dictionary=True)
        #Usiamo DISTINCT per non avere generi doppi nel menu a tendina
        query = "SELECT DISTINCT genere FROM libro ORDER BY genere"
        cursor.execute(query)

        result = []
        for row in cursor:
            if row["genere"]: #se non è vuoto
                result.append(row["genere"])

        cursor.close()
        cnx.close()
        return result

    def get_libri_filtrati(self, nome_biblioteca, genere) -> list[Libro]:
        cnx=DBConnect.get_connection()
        if cnx is None:
            return []

        cursor=cnx.cursor(dictionary=True)
        #uso join perchè l'utente sceglie il nome della biblioteca, ma nella tabella libri si trova solo l id_biblioteca
        query= """
            SELECT l.*
            FROM libro l
            JOIN biblioteca b ON l.id_biblioteca =b.id
             WHERE b.nome = COALESCE(%s, b.nome)
              AND l.genere = COALESCE(%s, l.genere)
            """

        cursor.execute(query, (nome_biblioteca, genere))
        result = []
        for row in cursor:
            l = Libro(
                id=row["id"],
                titolo=row["titolo"],
                autore=row["autore"],
                genere=row["genere"],
                anno_pubblicazione=row["anno_pubblicazione"],
                id_biblioteca=row["id_biblioteca"],
            )
            result.append(l)

        cursor.close()
        cnx.close()
        return result