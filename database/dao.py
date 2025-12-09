from database.DB_connect import DBConnect
from model.rifugio import Rifugio

class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO

    @staticmethod
    def get_all_rifugi() -> list[Rifugio] | None:
        """ Restituisce tutti i rifugi presenti nel database. """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM rifugio """
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(Rifugio(
                    id=row['id'],
                    nome=row['nome'],
                    localita=row['localita'],
                    altitudine=row['altitudine'],
                    capienza=row['capienza'],
                    aperto=row['aperto']
                ))
        except Exception as e:
            print(f"Errore DAO get_all_rifugi: {e}")
            result = None
        finally:
            if cursor: cursor.close()
            if cnx: cnx.close()

        return result

    @staticmethod
    def get_connessioni_fino_a(anno: int) -> list[dict] | None:
        """
        Restituisce tutte le connessioni (sentieri) create fino all'anno specificato.
        :return: Lista di dizionari [{'id_rifugio1', 'id_rifugio2', 'anno', ...}]
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return None

        # Filtriamo le connessioni con un anno <= all'anno specificato
        query = """ 
            SELECT 
                id_rifugio1, 
                id_rifugio2, 
                distanza, 
                difficolta, 
                durata, 
                anno 
            FROM connessione 
            WHERE anno <= %s
        """

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(query, (anno,))
            for row in cursor:
                result.append(row)
        except Exception as e:
            print(f"Errore DAO get_connessioni_fino_a: {e}")
            result = None
        finally:
            if cursor: cursor.close()
            if cnx: cnx.close()

        return result